import pyperclip
from bs4 import BeautifulSoup


def generate_javascript(html_file):

    with open(html_file, 'r') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')  # create a BeautifulSoup object

    # Extract all elements with an id attribute
    elements = []
    for element in soup.find_all(id=True):
        elements.append(element['id'])

    # Generate a line of JavaScript code for each element
    lines = []
    element_list = []
    for element in elements:
        if element not in element_list:
            temp_element = element.split('-')
            end_element = ''
            for ind, it in enumerate(temp_element):

                end_element += it.capitalize()

            # find the tag of the element
            element_tag = soup.find(id=element).name
            lines.append(
                f"const {element_tag}{end_element} = document.getElementById('{element}');")  # add the tag to the variable name
            element_list.append(element)


    js = '\n'.join(lines)
    pyperclip.copy(js)