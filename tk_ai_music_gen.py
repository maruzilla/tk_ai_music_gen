################################
# AI Music Generator
# 		tk_ai_music_gen.py
# 		by Dr.Maruzilla
################################

import tkinter as tk
from tkinter import ttk
from openai import OpenAI		# pip install --upgrade openai
import anthropic				# pip install anthropic
import google.generativeai as genai		# pip install -q -U google-generativeai
import pyperclip				# pip install pyperclip
import webbrowser

def generate_answer():
    # Get input text and combo box values ​​and create questions
    input_part = cbox_part.get().rstrip("\n")						# rstrip("\n") 	<- 改行を trim
    input_chord = txt_input_chord.get( 0., tk.END ).rstrip("\n")
    input_genre = txt_input_genre.get( 0., tk.END ).rstrip("\n")
    input_beat_len = cbox_beat_len.get().rstrip("\n")
    input_note_reso = cbox_note_reso.get().rstrip("\n")
    input_ai_model = cbox_ai_model.get().rstrip("\n")

    question = f"Please write a {input_part} melody that matches a song that repeats the chord progression\n" \
    		   f"' {input_chord} '. \n" \
    		   f"The song should be {input_genre} style," \
    		   f"the output format should be ABC-Notation, \nin {input_beat_len} time with {input_note_reso} notes per character."

    question_j = f"コード進行「{input_chord}」」を繰り返す曲に合う {input_part} の\nメロディーを書いて下さい。" \
 				 f"  曲調は、{input_genre} 風で、出力形式は \n" \
 				 f"{input_note_reso}拍子で、1文字が {input_beat_len}分音符の ABC-記譜法の形式であること。"

    # Show questions in labels
    label_question.config(text=question)
    label_question_j.config(text=question_j)
    pyperclip.copy(input_ai_model + "\n" + question + "\n" + question_j)
    
    # Send a question to ChatGPT / Claude / Gemini
    try:
        if input_ai_model == "GPT":
            ######### OpenAI / GPT 4o mini:  ↓ Paste your API-key (Don't share this!!) #########
            client = OpenAI(api_key="XXXXXXXXXXXXXXXX")
            response = client.chat.completions.create(
                model="gpt-4o-mini",		# <-x	"gpt-3.5-turbo"
                messages=[
                    {"role": "system", "content": "あなたは天才作曲家です。指定された文字数で回答してください。"},
                    {"role": "user", "content": question}
                ]
            )
            # Get answer
            answer = response.choices[0].message.content

        elif input_ai_model == "Claude":
            ######### Anthropic / Claude 3.5 Sonnet:  ↓ Paste your API-key (Don't share this!!) #########
            client = anthropic.Anthropic(api_key="XXXXXXXXXXXXXXXX")
            response = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000, 	# 出力上限（4096まで?） <- 要確認!!
                temperature=0.0, 	# 0.0-1.0
                system="あなたは天才作曲家です。指定された文字数で回答してください。", 			# 必要ならシステムプロンプトを設定
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            # Get answer
            answer = response.content[0].text

        elif input_ai_model == "Gemini":
            ######### Google / Gemini 1.5 Flash:  ↓ Paste your API-key (Don't share this!!) #########
            genai.configure(api_key="XXXXXXXXXXXXXXXX")
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(question)

            # Get answer
            answer = response.text

        ######## Set it Textbox
        txt_Answer.delete(1.0, tk.END)
        txt_Answer.insert(tk.END, answer)

    except Exception as e:
        error_message = f"エラーが発生しました (T_T;\n{str(e)}\n\n詳細:\n{type(e).__name__}: {str(e)}"
        txt_Answer.delete(1.0, tk.END)
        txt_Answer.insert(tk.END, error_message)
        print(error_message)  # コンソールにもエラーを出しておく

def copy_to_clipboard():
    answer = txt_Answer.get(1.0, tk.END)
    pyperclip.copy(answer)

def link_click():
    webbrowser.open_new("https://www.ne.jp/asahi/music/marinkyo/ml/abcjs-redaktilo.html.ja")

# Main window
root = tk.Tk()
root.title("AI Music Generator  by Dr.Maruzilla")


# Please write a main melody that matches a song that repeats the chord progression
# 'Fmaj7, Em7, Am7, G, Fmaj7, Em7, Dm7, Cmaj7'. 
# The song should be Chillout style, 
# the output format should be ABC-Notation, in 1/4 time with 1/16 notes per character.

# コード進行「Fmaj7, Em7, Am7, G, Fmaj7, Em7, Dm7, Cmaj7」を繰り返す曲に合う 主旋律のメロディーを書いて下さい。 
# 曲調は、Chillout風で、出力形式は 1/4拍子で、1文字が 16分音符の ABC-記譜法の形式であること。

	# _part,  _chord,  _genre,  _beat_len,  _note_reso

# Which part?	(ComboBox)
label_part = ttk.Label(root, text="Which part ? :")
label_part.grid(row=0, column=0)
cbox_part = ttk.Combobox(root, values=["main", "bass-line", "chorus"], state="readonly", width=20)
cbox_part.set("main")						# Default
cbox_part.grid(row=0, column=1)

# Chords		(Big TextBox)
label_input_chord = ttk.Label(root, text="Chords:")
label_input_chord.grid(row=1, column=0,)
txt_input_chord = tk.Text(root, height=4, width=50)
txt_input_chord.insert( 0., "Fmaj7, Em7, Am7, G, Fmaj7, Em7, Dm7, Cmaj7")		# Default
txt_input_chord.grid(row=1, column=1, columnspan=2)			# , padx=5, pady=5, sticky="w"

# Genre		(Entry TextBox)
label_input_genre = ttk.Label(root, text="Genre:")
label_input_genre.grid(row=2, column=0)
txt_input_genre = tk.Text(root, height=1, width=25)
txt_input_genre.insert( 0., "Chillout")				# Default
txt_input_genre.grid(row=2, column=1)

# Beat length	(ComboBox)
label_beat_len = ttk.Label(root, text="Beat length:")
label_beat_len.grid(row=3, column=0)
cbox_beat_len = ttk.Combobox(root, values=["1/4", "2/4", "3/4", "4/4"], state="readonly", width=20)
cbox_beat_len.set("1/4")						# Default
cbox_beat_len.grid(row=3, column=1)

# Notes resolution	(ComboBox)
label_note_reso = ttk.Label(root, text="Notes resolution:")
label_note_reso.grid(row=4, column=0)
cbox_note_reso = ttk.Combobox(root, values=["1/3", "1/4", "1/6", "1/8", "1/12", "1/16", "1/24"], state="readonly", width=20)
cbox_note_reso.set("1/16")						# Default
cbox_note_reso.grid(row=4, column=1)

# Question - En
label_question = ttk.Label(root, text="", width=80)
label_question.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

# Question - Ja
label_question_j = ttk.Label(root, text="", width=80)
label_question_j.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

# AI Model	(ComboBox)
label_ai_model = ttk.Label(root, text="Whitch AI Model ? :")
label_ai_model.grid(row=7, column=0)
cbox_ai_model = ttk.Combobox(root, values=["GPT", "Claude", "Gemini"], state="readonly", width=20)
cbox_ai_model.set("GPT")						# Default
cbox_ai_model.grid(row=7, column=1)

# Gen button
btn_Generate = ttk.Button(root, text="Generate melody!", command=generate_answer)
btn_Generate.grid(row=7, column=2)		#, columnspan=2, padx=5, pady=5

# Answer Textbox
txt_Answer = tk.Text(root, height=16, width=64)
txt_Answer.grid(row=8, column=0, columnspan=3)		# , padx=5, pady=5)

# Copy button
btn_Copy = ttk.Button(root, text="Copy", command=copy_to_clipboard)
btn_Copy.grid(row=10, column=1)

# Open ABC player
btn_link_abc = ttk.Button(root, text="Open ABC player", command=link_click)
btn_link_abc.grid(row=10, column=2)		# , columnspan=2, padx=5, pady=5)

# mainloop
root.mainloop()
