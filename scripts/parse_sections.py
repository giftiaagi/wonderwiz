import os
from bs4 import BeautifulSoup

from core.model.card import AdditionalContent, Image, Paragraph, Section, XHTMLDocument


def _remove_label_prefix(text: str, label: str) -> str:
    if text.startswith(f"【{label}】"):
        return text[len(f"【{label}】") :].strip()
    return text.strip()


def collect_sections_from_directory(directory_path: str) -> list[Section]:
    all_sections = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.startswith("Section0002_") and file.endswith(".xhtml"):
                file_path = os.path.join(root, file)
                xhtml_doc = parse_xhtml_document(file_path)
                all_sections.extend(xhtml_doc.sections)

    return all_sections


def parse_xhtml_document(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    soup = BeautifulSoup(content, "html.parser")
    sections = []

    for section_tag in soup.find_all(["h1", "h2"]):
        title = section_tag.text.strip()
        paragraphs = []
        images = []
        additional_content = AdditionalContent()  # 注意这里需要传递参数

        current_tag = section_tag.next_sibling
        while current_tag and current_tag.name not in ["h1", "h2"]:
            if current_tag.name == "p" and "bodycontent-text-wbs3" in current_tag.get(
                "class", []
            ):
                additional_content.weiboshi = _remove_label_prefix(
                    current_tag.text.strip(), "微博士"
                )
            elif current_tag.name == "p" and "bodycontent-text-gjz" in current_tag.get(
                "class", []
            ):
                keyword_content = current_tag.text.strip().split("】")
                if "微问题" in keyword_content[0]:
                    additional_content.weiwenti = _remove_label_prefix(
                        keyword_content[1].strip(), "微问题"
                    )
                elif "关键词" in keyword_content[0]:
                    keywords = (
                        keyword_content[1].strip().split("　")
                    )  # 使用中文空格分隔
                    additional_content.guanjianci = [
                        kw.strip() for kw in keywords if kw.strip()
                    ]

            elif (
                current_tag.name == "p"
                and "bodycontent-text-yinwen" in current_tag.get("class", [])
            ):
                additional_content.shiyanchang = _remove_label_prefix(
                    current_tag.text.strip(), "实验场"
                )
            elif (
                current_tag.name == "p"
                and "bodycontent-text-tushuo1" in current_tag.get("class", [])
            ):
                additional_content.kexueren = _remove_label_prefix(
                    current_tag.text.strip(), "科学人"
                )
            elif current_tag.name == "p":
                if current_tag.text.strip():
                    paragraphs.append(Paragraph(text=current_tag.text.strip()))
            elif current_tag.name == "div" and "tupian" in current_tag.get("class", []):
                image_tag = current_tag.find("img")
                if image_tag:
                    images.append(Image(src=image_tag.get("src", "")))

            current_tag = current_tag.next_sibling

        sections.append(
            Section(
                title=title,
                paragraphs=paragraphs,
                images=images,
                additional_content=additional_content,
            )
        )

    return XHTMLDocument(sections=sections)


if __name__ == "__main__":
    sections = collect_sections_from_directory("data/OEBPS/Text/")
    # doc1 = parse_xhtml_document("data/OEBPS/Text/Section0002_0002.xhtml")
    print(sections)
