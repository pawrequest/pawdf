import os
from argparse import ArgumentParser
from pathlib import Path

from pypdf import PaperSize, PdfReader, PdfWriter, Transformation
from pypdf.papersizes import Dimensions

ADDED_MARGIN = 0.2


def create_parser():
    parser = ArgumentParser(description='Array A6 PDFS on A4.')
    parser.add_argument('--input_path', '-i', required=True, type=Path, help='A6 PDF input path.')
    parser.add_argument(
        '--output_dir',
        '-o',
        type=Path,
        help='Output dir. Defaults to input/arrayed'
    )
    parser.add_argument('--print_files', action='store_true', help='Print the output.')
    return parser


def main(args=None):
    parser = create_parser()
    args = parser.parse_args(args)

    input_path = args.input_path.resolve()
    if not input_path.exists():
        raise ValueError(f'{input_path=} does not exist')
    print(f'{input_path=}')

    output_dir = args.output_dir.resolve() if args.output_dir else None
    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True)

    convert_many(input_path, output_dir=output_dir, print_files=args.print_files)


def convert_many(*input_files: Path, output_dir: Path = None, print_files=False):
    input_files = list(input_files)
    output_dir = output_dir or input_files[0].parent / 'arrayed'
    output_dir.mkdir(exist_ok=True)
    for file in input_files:
        output_file = output_dir / f'{file.stem}_on_a4.pdf'
        print(f'Processing {file.name} into {output_file}...')
        on_a4(file, output_file)
        if print_files:
            os.startfile(output_file, 'print')


def get_scale_factor(input_size: Dimensions, output_size: Dimensions) -> float:
    return min(
        [(output_size.width / input_size.height), (output_size.height / input_size.width)]
    ) / (1 + ADDED_MARGIN)


def on_a4(
        input_file: Path,
        output_file: Path,
        output_size=PaperSize.A4,
):
    if not input_file.is_file():
        raise ValueError(f'Invalid input file path {input_file} of type {type(input_file)}.')
    if output_file.suffix != '.pdf':
        raise ValueError('Ouput path not .pdf.')
    reader = PdfReader(input_file)

    input_size = Dimensions(reader.pages[0].mediabox.width, reader.pages[0].mediabox.height)
    scale_factor = get_scale_factor(input_size, output_size)
    resized = Dimensions(
        int(scale_factor * input_size.width),
        int(scale_factor * input_size.height)
    )

    left_translation, right_translation = get_translations(resized, output_size)

    writer = PdfWriter()

    for i in range(0, len(reader.pages), 2):
        # width and height are swapped for landscape
        d_page = writer.add_blank_page(output_size.height, output_size.width)
        for j in range(2):
            if i + j < len(reader.pages):
                page_num = i + j
                translate_ = left_translation if j == 0 else right_translation  # zero-indexed so swap left right vs even odd
                page = reader.pages[page_num]
                page.scale_by(scale_factor)
                d_page.merge_transformed_page(page, translate_)

    with open(output_file, 'wb') as out_pdf_file:
        writer.write(out_pdf_file)


def get_translations(in_size: Dimensions, out_size: Dimensions) -> tuple[
    Transformation, Transformation]:
    x_left, x_right, y = get_translation_dims(in_size, out_size)
    return (Transformation().translate(x_left, y),
            Transformation().translate(x_right, y))


#
def get_translation_dims(in_size: Dimensions, out_size: Dimensions) -> tuple[float, float, float]:
    translate_x_left = (out_size.height / 2 - in_size.width) / 2
    translate_x_right = (out_size.height / 2 - in_size.width) / 2 + out_size.height / 2
    translate_y = (out_size.width - in_size.height) / 2

    return translate_x_left, translate_x_right, translate_y


if __name__ == '__main__':
    main()
