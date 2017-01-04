



def JsonResult(title, content):
    sentences = Paragraph_to_Sentences (content)

    return title + ','+ content + ','+ 'success!'