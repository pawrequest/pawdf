from argparse import ArgumentParser
from pathlib import Path

from pawdf import array_pdfs


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

    array_pdfs(input_path, output_dir=output_dir, print_files=args.print_files)


if __name__ == '__main__':
    main()
