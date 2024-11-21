from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

phonemes = """
Phonemes

IPA Phoneme	X-SAMPA Phoneme	Example Word	IPA	X-SAMPA
p	popular	"pQpj@l@
b	bubble	"bVb@l
t	tinker	"tINk@
d	Dundee	%dVn"di:
k	crown	"kr\aUn
g	gravely	ˈgɹeɪˌvliː	"gr\eI%vli:
m	mapping	ˈmæpəŋ	"m{p@N
n	nine	ˈnaɪn	"naIn
N	bank	ˈbæŋk	"b{Nk
f	frog	ˈfɹɒg	"fr\Qg
v	valve	ˈvælv	"v{lv
s	massage	məˈsɑːʒ	m@"sA:Z
z	zoom	ˈzuːm	"zu:m
T	thigh	ˈθaɪ	"TaI
D	mother	ˈmʌðə	"mVD@
S	shopping	ˈʃɒpəŋ	"SQp@N
Z	leisure	ˈlɛʒə	"lEZ@
h	mahogany	məˈhɒgəˌniː	m@"hQg@%ni:
l	lately	ˈleɪtˌliː	"leIt%li:
r\	roaring	ˈɹɔːɹəŋ	"r\O:r\@N
tS	changed	ˈʧeɪnʤd	"tSeIndZd
dZ	magenta	məˈʤɛntə	m@"dZEnt@
j	younger	ˈjʌŋgə	"jVNg@
w	whirlwind	ˈwɜːlˌwɪnd	"w3:l%wInd
{	cat	ˈkæt	"k{t
A:	car	ˈkɑː	"kA:
@	again	əˈgɛn	@"gEn
E	bed	ˈbɛd	"bEd
I	kit	ˈkɪt	"kIt
i:	unique	ˌjuːˈniːk	%ju:"ni:k
Q	yacht	ˈjɒt	"jQt
O:	caught	ˈkɔːt	"kO:t
U	could	ˈkʊd	"kUd
u:	school	ˈskuːl	"sku:l
V	pulse	ˈpʌls	"pVls
3:	nurse	ˈnɜːs	"n3:s
aI	price	ˈpɹaɪs	"pr\aIs
aU	flower	ˈflaʊə	"flaU@
eI	shade	ˈʃeɪd	"SeId
e@	square	ˈskweə	"skwe@
i@	near	ˈniə	"ni@
OI	choice	ˈʧɔɪs	"tSOIs
@U	boat	ˈbəʊt	"b@Ut
U@	cure	ˈkjʊə	"kjU@
Levels of stress
Symbol	X-SAMPA
Primary stress  "
Secondary stress    %
Syllable boundary   .
"""

phoneme_instructions = """
<phoneme>
You can use the <phoneme> tag to produce custom pronunciations of words inline. Text-to-Speech accepts the IPA phonetic alphabet. 

Each application of the <phoneme> tag directs the pronunciation of a single word:

  <phoneme alphabet="ipa" ph="ˌmænɪˈtoʊbə">manitoba</phoneme>
  <phoneme alphabet="x-sampa" ph='m@"hA:g@%ni:'>mahogany</phoneme>

Stress markers
There are up to three levels of stress that can be placed in a transcription:

Primary stress: Denoted with /ˈ/ 
Secondary stress: Denoted with /ˌ/ 
Unstressed: Not denoted with a symbol (in either notation).


Example word	
water	ˈwɑːtɚ	
underwater	ˌʌndɚˈwɑːtɚ

Broad vs Narrow Transcriptions
As a general rule, keep your transcriptions more broad and phonemic in nature. For example, in US English, transcribe intervocalic /t/ (instead of using a tap):

Example word	
butter	ˈbʌtɚ instead of ˈbʌɾɚ	
There are some instances where using the phonemic representation makes your TTS results sound unnatural (for example, if the sequence of phonemes is anatomically difficult to pronounce).

One example of this is voicing assimilation for /s/ in English. In this case the assimilation should be reflected in the transcription:

Example word	
cats	ˈkæts	
dogs	ˈdɑːgz instead of ˈdɑːgs

Reduction
Every syllable must contain one (and only one) vowel. This means that you should avoid syllabic consonants and instead transcribe them with a reduced vowel. For example:

Example word
kitten	ˈkɪtən instead of ˈkɪtn
kettle	ˈkɛtəl instead of ˈkɛtl

Syllabification
You can optionally specify syllable boundaries by using /./. Each syllable must contain one (and only one) vowel. For example:

Example word
readability	ˌɹiː.də.ˈbɪ.lə.tiː	
"""
#automatically looks for an "ANTHROPIC_API_KEY" environment variable
client = Anthropic()

def repeat_words(data, chat, question):
    try:
        EXERCISE_DETAILS = data['exercise_details']
        prompt = f"""
You are an AI assistant for a charity program that teaches literacy to ex-convicts. Your role is to provide helpful feedback and assistance when users request help during their exercises. The current exercise involves the user repeating a word vocally, which is then converted to text using speech recognition.

Here are the details of the current exercise:
<exercise_details>
{EXERCISE_DETAILS}
</exercise_details>

Here is a history of your chat so far.
<chat>
{chat}
</chat>

The user has asked the following question:
<user_question>
{question}
</user_question>

Your task is to generate a helpful response based on the exercise details and the user's request. 

You should use phonemes to help explain words where appropriate. In the example phonemes, you can see the example phonmene, an example of a word that uses it, and also the phoneme breakdown of the whole word example. 
Please note that all characters in the phoneme list are relevant, for example, the second syllable of happy would be <phoneme alphabet="ipa" ph="pi:">py</phoneme>, not <phoneme alphabet="ipa" ph="pi">py</phoneme>
Some phonemes from <phonemes> includ ' and , which are used to denote stress and syllable breaks and should be included in the phoneme when describing a single letter, eg: pay <phoneme alphabet="ipa" ph=",p">py</phoneme>
Here are the phonemes you can use:

<phonemes>
{phonemes}
</phonemes>

Here are instructions on how to include the phonemes in you response:

<phoneme_instructions>
{phoneme_instructions}
</phoneme_instructions>

Follow the instructions provided inside the <instructions> tags below when answering questions.

<instructions>
1. Be encouraging and supportive in your tone.
2. If the user is asking about a specific word, provide a clear and simple explanation.
3. If appropriate, suggest words that sound similar to help with pronunciation or understanding.
4. Offer tips on how to approach the exercise if the user seems confused.
5. Keep your response short and easy to understand, considering the user's literacy level.
6. Do not provide any information or assistance beyond what's relevant to the current exercise and the user's specific request.
7. The user is presented with the words in 'data' and must select them one at a time and records themselves saying the word.
8. Do not use quotes for examples, rather use commas before and after each example or sound
9. If you're giving a word broken down into sounds, use "<phoneme></phoneme>, followed by, <phoneme></phoneme>" instead of +. For example: <phoneme alphabet="ipa" ph="ʧ">ch</phoneme> followed by <phoneme alphabet="ipa" ph="eɪn">ain</phoneme>
10. If you want to say something like 'a long e sound' or 'a long a sound', use the phoneme for the vowel sound followed by 'long' and the name of the vowel. For example: 'long e' becomes 'long <phoneme alphabet="ipa" ph="iːi:">e</phoneme> or 'long a' becomes long <phoneme alphabet="ipa" ph="eɪ">a</phoneme>
11. After every closing </phoneme> tag, add a self closing <break time="250ms"/> tag
Formulate your response as a string that can be printed and synthesized into audio feedback using the phonemes provided in <phonemes> using the instructions provided in <phoneme_instuctions>. The response should be clear, helpful, and directly address the user's request while taking into account the exercise details.
</instructions>

Present your response within <speak> tags within <answer> tags. Do not include any other text or explanations outside of these tags.
"""
        response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": prompt}        
        ]
    )
        print(response)
        if response.content[0].text:
            return response.content[0].text
        else:
            return "error"
        
    except Exception as e:
        return f"Error: {str(e)}"