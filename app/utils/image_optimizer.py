from PIL import Image
import io
import os
from pathlib import Path

def optimize_and_convert_to_webp(image_path: str, quality: int = 85) -> str:
    """
    Convert uploaded image to WebP format with optimization
    
    Args:
        image_path: Path to original image
        quality: WebP quality (1-100, default 85)
    
    Returns:
        Path to optimized WebP image
    """
    try:
        # Open image
        img = Image.open(image_path)
        
        # Convert RGBA to RGB if needed
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Resize if too large (max 1920px width)
        max_width = 1920
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Generate WebP path
        webp_path = Path(image_path).with_suffix('.webp')
        
        # Save as WebP
        img.save(
            webp_path,
            'WEBP',
            quality=quality,
            method=6,  # Best compression
            optimize=True
        )
        
        # Delete original if conversion successful
        if webp_path.exists() and os.path.getsize(webp_path) > 0:
            os.remove(image_path)
            return str(webp_path)
        
        return image_path
        
    except Exception as e:
        print(f"Image optimization failed: {str(e)}")
        return image_path


def create_thumbnail(image_path: str, size: tuple = (400, 300)) -> str:
    """Create thumbnail version for faster loading"""
    try:
        img = Image.open(image_path)
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        thumb_path = Path(image_path).parent / f"thumb_{Path(image_path).name}"
        img.save(thumb_path, 'WEBP', quality=80, optimize=True)
        
        return str(thumb_path)
    except Exception as e:
        print(f"Thumbnail creation failed: {str(e)}")
        return image_path