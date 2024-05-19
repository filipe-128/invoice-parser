from paddleocr import PaddleOCR, draw_ocr
from PIL import Image

def start_paddle_ocr():
    """Starts paddle OCR engine."""
    paddle_ocr = PaddleOCR(binarize=False,
                           invert=False,
                           det_db_score_mode='slow',
                           ocr_version='PP-OCRv4',
                           save_crop_res=False,
                           lang='pt',
                           max_text_length=50,
                           drop_score=0.5,
                           use_angle_cls=False,
                           use_gpu=True,
                           show_log=False,
                           det_limit_side_len=2000,
                           use_space_char=True
                           )

    return paddle_ocr

def run_paddle_ocr(imgpath, temp_dir, paddle_ocr=None):
    """Runs the OCR engine and obtains dictionary with results."""
    # Downloads and loads model into memory
    if paddle_ocr is None:
        paddle_ocr = start_paddle_ocr()

    # Run OCR
    result = paddle_ocr.ocr(imgpath, cls=False)
    result = result[0]
    if result is not None:
        image = Image.open(imgpath).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path='media/OpenSans-Regular.ttf')
        im_show = Image.fromarray(im_show)
        im_show.save(f'{temp_dir}/ocr_result.jpg')

    return result
