from py_translator import Translator

# Define the text to be translated
text = "Hello, how are you?"

# Define the target language (in this case, Spanish)
target_language = 'es'

# Translate the text
translation = Translator().translate(text=text, dest=target_language)

# Print the translation
print(translation.text)
