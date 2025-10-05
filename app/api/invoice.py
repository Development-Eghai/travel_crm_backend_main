from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.invoice import InvoiceCreate
from models.invoice import Invoice, InvoiceItem, InvoicePayment
from core.database import get_db
from utils.response import api_json_response_format
from datetime import date

router = APIRouter()

@router.post("/")
def create_invoice(invoice_in: InvoiceCreate, db: Session = Depends(get_db)):
    try:
        invoice_number = invoice_in.invoice_number or f"INV-{date.today().strftime('%Y%m%d')}-{invoice_in.lead_id}"

        subtotal = sum(i.quantity * i.unit_price for i in invoice_in.items)
        discount_total = 0
        for i in invoice_in.items:
            if i.discount_type == "percent":
                discount_total += (i.quantity * i.unit_price) * (i.discount / 100)
            else:
                discount_total += i.discount

        taxable_amount = subtotal - discount_total
        gst_total = sum((taxable_amount * i.gst_percent / 100) for i in invoice_in.items)

        if invoice_in.is_interstate:
            igst = gst_total
            cgst = sgst = 0
        else:
            cgst = sgst = gst_total / 2
            igst = 0

        total_amount = taxable_amount + gst_total
        paid_amount = invoice_in.payment.amount if invoice_in.payment else 0
        due_amount = total_amount - paid_amount

        invoice = Invoice(
            lead_id=invoice_in.lead_id,
            quotation_id=invoice_in.quotation_id,
            client_name=invoice_in.client_name,
            client_email=invoice_in.client_email,
            client_phone=invoice_in.client_phone,
            client_gst=invoice_in.client_gst,
            client_address=invoice_in.client_address,
            invoice_number=invoice_number,
            invoice_date=invoice_in.invoice_date,
            due_date=invoice_in.due_date,
            is_interstate=invoice_in.is_interstate,
            subtotal=subtotal,
            discount=discount_total,
            taxable_amount=taxable_amount,
            cgst=cgst,
            sgst=sgst,
            igst=igst,
            total_amount=total_amount,
            due_amount=due_amount,
            template=invoice_in.template,
            terms_and_conditions=invoice_in.terms.terms_and_conditions,
            payment_terms=invoice_in.terms.payment_terms,
            cancellation_policy=invoice_in.terms.cancellation_policy,
            notes=invoice_in.terms.notes
        )
        db.add(invoice)
        db.commit()
        db.refresh(invoice)

        for item in invoice_in.items:
            db.add(InvoiceItem(
                invoice_id=invoice.id,
                item_name=item.item_name,
                description=item.description,
                hsn_code=item.hsn_code,
                quantity=item.quantity,
                unit_price=item.unit_price,
                discount=item.discount,
                discount_type=item.discount_type,
                gst_percent=item.gst_percent
            ))

        if invoice_in.payment:
            db.add(InvoicePayment(
                invoice_id=invoice.id,
                amount=invoice_in.payment.amount,
                method=invoice_in.payment.method,
                date=invoice_in.payment.date,
                transaction_id=invoice_in.payment.transaction_id,
                notes=invoice_in.payment.notes
            ))

        db.commit()

        return api_json_response_format(True, "Invoice created successfully.", 201, {"invoice_id": invoice.id})

    except Exception as e:
        return api_json_response_format(False, f"Error creating invoice: {e}", 500, {})
    
@router.get("/")
def get_all_invoices(db: Session = Depends(get_db)):
    try:
        invoices = db.query(Invoice).order_by(Invoice.invoice_date.desc()).all()
        data = [
            {
                "id": inv.id,
                "invoice_number": inv.invoice_number,
                "client_name": inv.client_name,
                "invoice_date": inv.invoice_date,
                "due_date": inv.due_date,
                "amount": inv.total_amount,
                "status": "Paid" if inv.due_amount == 0 else "Unpaid",
            }
            for inv in invoices
        ]
        return api_json_response_format(True, "Invoices retrieved successfully.", 200, data)
    except Exception as e:
        return api_json_response_format(False, f"Error retrieving invoices: {e}", 500, {})
    
@router.get("/{invoice_id}")
def get_invoice_by_id(invoice_id: int, db: Session = Depends(get_db)):
    try:
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            return api_json_response_format(False, "Invoice not found", 404, {})

        data = {
            "id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "lead_id": invoice.lead_id,
            "quotation_id": invoice.quotation_id,
            "client_name": invoice.client_name,
            "client_email": invoice.client_email,
            "client_phone": invoice.client_phone,
            "client_gst": invoice.client_gst,
            "client_address": invoice.client_address,
            "invoice_date": invoice.invoice_date,
            "due_date": invoice.due_date,
            "is_interstate": invoice.is_interstate,
            "subtotal": invoice.subtotal,
            "discount": invoice.discount,
            "taxable_amount": invoice.taxable_amount,
            "cgst": invoice.cgst,
            "sgst": invoice.sgst,
            "igst": invoice.igst,
            "total_amount": invoice.total_amount,
            "due_amount": invoice.due_amount,
            "template": invoice.template,
            "terms_and_conditions": invoice.terms_and_conditions,
            "payment_terms": invoice.payment_terms,
            "cancellation_policy": invoice.cancellation_policy,
            "notes": invoice.notes,
            "items": [
                {
                    "item_name": i.item_name,
                    "description": i.description,
                    "hsn_code": i.hsn_code,
                    "quantity": i.quantity,
                    "unit_price": i.unit_price,
                    "discount": i.discount,
                    "discount_type": i.discount_type,
                    "gst_percent": i.gst_percent
                }
                for i in invoice.items
            ],
            "payments": [
                {
                    "amount": p.amount,
                    "method": p.method,
                    "date": p.date,
                    "transaction_id": p.transaction_id,
                    "notes": p.notes
                }
                for p in invoice.payments
            ]
        }

        return api_json_response_format(True, "Invoice retrieved successfully.", 200, data)

    except Exception as e:
        return api_json_response_format(False, f"Error retrieving invoice: {e}", 500, {})
    
@router.put("/{invoice_id}")
def update_invoice(invoice_id: int, invoice_in: InvoiceCreate, db: Session = Depends(get_db)):
    try:
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            return api_json_response_format(False, "Invoice not found", 404, {})

        # Update core fields
        for key, value in invoice_in.model_dump(exclude={"items", "terms", "payment"}).items():
            setattr(invoice, key, value)

        # Update terms
        invoice.terms_and_conditions = invoice_in.terms.terms_and_conditions
        invoice.payment_terms = invoice_in.terms.payment_terms
        invoice.cancellation_policy = invoice_in.terms.cancellation_policy
        invoice.notes = invoice_in.terms.notes

        # Clear and re-add items
        db.query(InvoiceItem).filter_by(invoice_id=invoice.id).delete()
        for item in invoice_in.items:
            db.add(InvoiceItem(invoice_id=invoice.id, **item.model_dump()))

        # Clear and re-add payment
        db.query(InvoicePayment).filter_by(invoice_id=invoice.id).delete()
        if invoice_in.payment:
            db.add(InvoicePayment(invoice_id=invoice.id, **invoice_in.payment.model_dump()))

        db.commit()
        db.refresh(invoice)

        return api_json_response_format(True, "Invoice updated successfully.", 200, {"invoice_id": invoice.id})

    except Exception as e:
        return api_json_response_format(False, f"Error updating invoice: {e}", 500, {})
    
@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    try:
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            return api_json_response_format(False, "Invoice not found", 404, {})

        db.delete(invoice)
        db.commit()

        return api_json_response_format(True, "Invoice deleted successfully.", 200, {})

    except Exception as e:
        return api_json_response_format(False, f"Error deleting invoice: {e}", 500, {})