import io
import tempfile
from PIL import Image
def save_image_to_temp_file(image_data: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        image = Image.open(io.BytesIO(image_data))
        image.save(temp_file, format="PNG")
        return temp_file.name
import re
async def consume_async_generator(generator):
    async for item in generator:
        yield item