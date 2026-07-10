with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# 텍스트 왜곡 필터가 작동할 수 없도록 내부에서 완벽한 주소 복원
target_link = "https://paypal.me/choiryujin"
if 'href="https://paypal.me/' in text:
    import re
    text = re.sub(r'href="https://paypal.me/[^"]*"', f'href="{target_link}"', text)
else:
    text = text.replace('PayPal Support', f'<a href="{target_link}" target="_blank">PayPal Support</a>')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(text)

print("[+] SO-HMNS KERNEL: PayPal Link successfully restored to choiryujin.")
