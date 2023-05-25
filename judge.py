import random
import re



def is_more_than_30_chars(message):
    return len(message) >= 30



# bug: 大きな素数を入れると処理に時間がかかる（例 2147483647）
def contains_prime_number(message):
    # 文章中の整数nを順番に取り出す
    for n in map(int, re.findall(r'\d+', message)):
        # nが2未満ならスキップ
        if n < 2:
            continue
        # nが2≦i<nで割り切れるかチェック
        is_prime = True
        for i in range(2, n):
            if n % i == 0:
                is_prime = False
                break
        
        if is_prime:
            return True

    return False



def contains_junishi_animal(message):
    return False



def get_random_NG():
    return random.choice([
        ('30文字以上の文章', is_more_than_30_chars),
        ('素数を含む文章', contains_prime_number),
        ('十二支の動物を含む文章', contains_junishi_animal),
    ])