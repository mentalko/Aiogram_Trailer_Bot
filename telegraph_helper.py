from telegraph import Telegraph

def create_page(datas):
    telegraph = Telegraph()
    token = telegraph.create_account(short_name='englishclub')
    image = telegraph.upload_file('concat.jpg')
    print (image)
    
    article = '<img src="{}"/>'.format(image[0]['src'])
    for data in datas:
        article += '<figure><iframe src="/embed/youtube?url={}"></iframe></figure>'.format( data['url'])
    article += "<a href='{}'>...</a>"

    response = telegraph.create_page(
        'Трейлеры к фильмам',
        html_content=article
    )
    return response['url']