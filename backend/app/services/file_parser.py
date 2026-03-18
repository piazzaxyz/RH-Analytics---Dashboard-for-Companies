import csv
import io
from PyPDF2 import PdfReader
import json
from typing import Union, BinaryIO, TextIO

def parse_csv(file_obj: Union[str, BinaryIO, TextIO]) -> list:
	if hasattr(file_obj, 'read'):
		file_obj.seek(0)
		content = file_obj.read()
		if isinstance(content, bytes):
			content = content.decode('utf-8')
		return list(csv.DictReader(io.StringIO(content)))
	with open(file_obj, 'r', encoding='utf-8') as f:
		return list(csv.DictReader(f))

def parse_json(file_obj: Union[str, BinaryIO, TextIO]) -> list:
	if hasattr(file_obj, 'read'):
		file_obj.seek(0)
		data = json.load(file_obj)
	else:
		with open(file_obj, "r", encoding="utf-8") as f:
			data = json.load(f)
	if isinstance(data, list):
		return data
	return [data]

def parse_pdf(file_obj: Union[str, BinaryIO]) -> list:
	reader = PdfReader(file_obj)
	text = "\n".join([page.extract_text() or "" for page in reader.pages])
	records = [{"raw": line.strip()} for line in text.split("\n") if line.strip()]
	return records
