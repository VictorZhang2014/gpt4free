import g4f


# normal response
# response = g4f.ChatCompletion.create(model=g4f.Model.gpt_4, messages=[
#                                      {"role": "user", "content": "hi"}]) # alterative model setting
# print(response)

def main():
  response = g4f.ChatCompletion.create(model=g4f.Model.gpt_4, messages=[
                                      {"role": "user", "content": "Hello world"}], stream=True)
  for message in response:
      print(message)

 
main()

