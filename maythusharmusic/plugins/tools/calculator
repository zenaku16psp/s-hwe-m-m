from pyrogram import Client, filters
from pyrogram.types import Message
from maythusharmusic import app

# ဂဏန်းတွက်ရန် အသုံးပြုမည့် သင်္ကေတများ
ALLOWED_CHARS = "0123456789+-*/().%^ "

# filters.group ကို ဖြုတ်လိုက်ပါသည် (Private မှာပါ ရအောင်)
@app.on_message(filters.text & filters.group)
async def calculator_func(client: Client, message: Message):
    # စာသားမရှိလျှင် (သို့) Command ဖြစ်နေလျှင် ကျော်သွားမည်
    if not message.text or message.text.startswith("/"):
        return

    # စာသားထဲတွင် ဂဏန်းနှင့် သင်္ကေတများသာ ပါဝင်ကြောင်း စစ်ဆေးခြင်း
    expression = message.text.strip()
    
    # အနည်းဆုံး ဂဏန်းတစ်ခုနှင့် သင်္ကေတတစ်ခု ပါမှ တွက်ပေးမည်
    if not any(char.isdigit() for char in expression):
        return
    if not any(op in expression for op in "+-*/^%"):
        return

    # ခွင့်ပြုထားသော စာလုံးများသာ ပါဝင်ရမည်
    if not all(char in ALLOWED_CHARS for char in expression):
        return

    try:
        # ^ ကို power (**) အဖြစ် ပြောင်းလဲခြင်း
        calc_expression = expression.replace("^", "**")
        
        # တွက်ချက်ခြင်း
        result = eval(calc_expression)
        
        # ရလဒ်က round number ဖြစ်နေရင် .0 ဖြုတ်မည်
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        # အဖြေပြန်ပို့ခြင်း (Reply မထောက်ဘဲ ပို့မည်)
        await client.send_message(
            chat_id=message.chat.id,
            text=f"{expression} = {result}"
        )

    except Exception:
        pass
