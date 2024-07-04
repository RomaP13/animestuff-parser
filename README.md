# Novel Website Parser

This project is a parser for a novel website designed to enhance the search and retrieval of novels.
The website's native tools are insufficient for efficient searching, so this parser offers an improved solution.
It supports both synchronous and asynchronous parsing, with the async parser being approximately 8 times faster.

## Features

- **Synchronous Parsing**: Basic parsing of the novel website.
- **Asynchronous Parsing**: Enhanced performance with async parsing, approximately 8 times faster than synchronous.
- **Data Storage**: Extracted data is saved in `data/novels_data.json`.
- **Error Handling**: Robust error handling for fetching and parsing novel data.
- **Logging**: Comprehensive logging for monitoring and debugging.

## Dependencies

This project uses the following libraries:

- `requests`
- `beautifulsoup4`
- `lxml`
- `aiohttp`

## Installation

1. Clone the repository:
   
```bash
git clone git@github.com:RomaP13/animestuff-parser.git
cd animestuff-parser/
```

2. Install dependencies using pipenv:

```bash
pipenv install
```

## Usage

### Synchronous Parsing

To run the synchronous parser:

```bash
make parse
```

### Asynchronous Parsing

To run the asynchronous parser:

```bash
make async_parse
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
