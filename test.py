# top_coins = ['dfkjbvk', 'skdfhbv']
# response_message = str(top_coins)[1:-1].replace(',', '').replace("'", '')
# print(response_message)

top_coins = ['dfkjbvk', 'skdfhbv', 'dfkjbvk', 'skdfhbv']
# response_message = str(top_coins)[2:-2].replace("', '", ', ')
response_message = ', '.join(top_coins)
print(response_message)
