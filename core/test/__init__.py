def get_company_form(file):
    return {
        'name': 'The Company',
        'description': 'All the best company',
        'phone': '24555432',
        'address': 'All the Address',
        'available_now': 'SI',
        'photo':  file,
        'category':  '1',
        'limits': '{"north": -32.754954,"east": -68.399872,"south": -32.758975,"west": -68.404060}',
        'payment_method':['1']
    }

def get_products_form(file):
    return {
        'name': 'The Product',
        'description': 'test Product',
        'price': '250',
        'is_available': 'SI',
        'photo':  file

    }
