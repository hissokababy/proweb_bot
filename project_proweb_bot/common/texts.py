
texts = {
    'ru': {

    'welcome': 
            {
        
        'hello_msg': 'Вас приветсвует центр современных профессий <b>PROWEB!</b>🤗',

        'greeting': f'''
Данный бот разработан специально для студентов центра <b>PROWEB.</b>

Возможности бота:

▪️ <b>Отправить текстовое сообщение</b> - задать любой вопрос, связанный с вашим обучением, и получить обратную связь
в ближайщее время.

▪️ <b>Тех. поддержка</b> - связаться с технической поддержкой и решить вопросы, связанные с компьютерной техникой. Также можно получить
консультацию и помощь в сборке личного компьютера.

▪️ <b>Коворкинг</b> - связаться с коворкинг админстратором и забронировать место на посещение.

▪️ <b>Конкурсы </b> - принять участие в ежемесячных конкурсах, где можно выиграть ценные призы.

▪️ <b>Посетить сайт</b> - переход на страницу центра PROWEB, где вы найдете всю подробную информацию о центре и о доступных курсах.

▪️ <b>Базовый курс</b> - записаться на бесплатный базовый курс компьютерной грамотности.

▪️ <b>Оставить отзыв</b> - возможность поделиться приятными впечетлениями об обучении в центре PROWEB. Если столкнулись с трудностями,
можно оставить жалобу или пожелание. Мы благодарны каждому отзыву.

▪️ <b>Правила обучения</b> - подробная информация о правилах обучения в центре PROWEB.

▪️ <b>На главную</b> - возможность вернуться на главную страницу бота и увидеть все его возможности.

▪️ <b>O'zbek tili</b> - переключение языка с русского на узбекский.

▪️ <b>Поделиться контактом</b> - если ваш вопрос имеет личный характер, оставьте свои данные и администрация центра
свяжется с вами лично в ближайщее время.
'''},

    'konkursi': {
        'photo': '',
        'text': f'''

Ежемесячно для студентов центра <b>PROWEB</b> проводятся конкурсы с ценными призами!🎉

<a href="https://proweb.uz/img/bonusMob.48c11c86.webp">&#8205;</a>

Для участия в конкурсах важно оставаться подписанным на нашего бота.

Подробные объявления с условиями конкурсов будут приходить личным сообщением всем подписчикам. Для того, чтобы оставаться
подписанным, достаточно просто не удалять и не блокировать бота.

Также мы проводим дополнительные  конкурсы длянаших подчисчиков в Instagram, Youtube, Telegram, Facebook - подписывайтесь
и участвуйте сразу в нескольких конкурсах.

Всех удачи, шанс выиграть есть у каждого студента!🍀
''',
    }
    ,


    'base_course': f'''
    Вы ссовершенно не разбираетесь в компьютере, но при этом хотите обучаться в <b>PROWEB?</b>
С нашим базовым курсом это возможно. Для этого вам просто необходимо нажать на кнопку "<b>Записаться на базовый курс</b>"
и наш преподаватель вас подробно обо всём проконсультрует.
<a href="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbOUYyx-etIXXSqfPAqohjX0LuKCUWjPWj9A&s">&#8205;</a>
    ''',


    'wishes': f'''
Вам нравится обучение в центре <b>PROWEB</b> и вам не трудно поделится об этом в наших социальных сетях? Тогда переходите по ссылке "<b>Отзывы</b>"
и опишите свои впечатления, мы будем очень признательны.

У вас возникли трудности во время обучения или вам что-то не понравилось, а может есть предложения и пожелания? Тогда переходите пл ссылке "<b>Жалобы и пожелания</b>",
распишите подробнее и мы сделаем все возможное, чтобы улучшить наш учебный центр.
''',

    'reply_btns': 
    
    {'main': [
        
        {'text': 'На главную ↩️', 'request_contact': None},
        {'text': "O'zbek tili 🇺🇿", 'request_contact': None},
        {'text': "Поделится контактом", 'request_contact': True},

    ]},


    'inline_btns': 
    
    {'main': [
        
        {'text': 'Тех. поддержка', 'url': 't.me/itsmylifestyle', 'callback_data': None},
        {'text': "Коворкинг", 'url': 't.me/proweb_coworking', 'callback_data': None},
        {'text': "Конкурсы🎉", 'url': None, "callback_data":'konkursi'},
        {'text': "Посетить сайт", 'url': 'proweb.uz', 'callback_data': None},
        {'text': "Базовый курс", 'url': None, 'callback_data': 'base_course'},
        {'text': "Оставить отзыв", 'url': None, 'callback_data': 'comment'},
        {'text': "Правила обучния", 'url': 't.me/proweb_coworking', 'callback_data': None},

    ],
    
        'base_course': [{'text': 'Записаться на Базовый курс', 'url': 't.me/proweb_basics', 'callback_data': None}],

        'wishes': [
            {'text': 'Отзывы 😍', 'url': 'https://proweb.uz/reviews/', 'callback_data': None},
            {'text': 'Жалобы и пожелания 😔', 'url': 'https://proweb.uz/reviews/', 'callback_data': None},
            ],

    },


    

    },




    'uz': 
    {
        'welcome': {
        
        'hello_msg': '<b>PROWEB</b> zamonaviy kasblar markaziga xush kelibsiz!🤗',
        
        'greeting': f'''
Bu bot maxsus <b>PROWEB</b> markazi talabalari uchun yaratilgan.

Bot imkoniyatlari:

▪️ <b>Matnli xabar yuboring</b> - mashg'ulotingiz bilan bog'liq har qanday savolni bering 
va iloji boricha tezroq qayta aloqa oling.

▪️ <b> Texnik yordam</b> - texnik yordam bilan bog'laning va kompyuter texnologiyalari bilan bog'loq muammolarni hal qiling.
Shuningdek, siz shaxsiy kompyuterni yig'ish bo'yicha maslahat va yordam oling.

▪️ <b>Kovorking</b> - kovorking administratoriga murojaat qiling va tashrif bbuyurishga joyni bron qiling.

▪️ <b>Tanlovlar</b> - har oylik tanlovlarda qatnashib, qimmatbaho sovrinlarni yutib oling.

▪️ <b>Saytga tashrif buyuring</b> - PROWEB markazining sahifasiga o'ting, u erda siz markaz va mavjud kurslar haqidagi barcha batafsil ma'lumotlarni topasiz.

▪️ <b>Kompyuter asoslari</b> - kompyuter asoslari kursiga yozilish.

▪️ <b>Sharh qoldiring</b> - PROWEB markazida mashg'ulotlardan yoqimli taassurotlar bilan bo'lishish imkoniyati. Agar
qiyinchiliklarga duch kelsangiz, shikoyat yoki so'rov qoldirishingiz mumkin. Biz har bir fikr uchun minnatdormiz.

▪️ <b>O'qish qoidalari</b> - PROWEB markazida o'qish qoidalari haqida batafsil ma'lumot.

▪️ <b>Bosh sahifaga</b> - botning asosiy sahifasiga qaytish va imkoniyatlari haqida batafsil ma'lumot olish.

▪️ <b>O'zbek tili</b> - tilni o'zbek tilidan rus tiliga o'tkazish.

▪️ <b>Kontakt bilan ulashing</b> - agar sizning savolingiz shaxsiy xarakterga ega bo'lsa, ozma'lumotlaringizni qoldiring va
markaz ma'muriyati imkon qadar tezroq siz bilan shaxsan bog'lanadi. 
'''},

    'konkursi': {
        'photo': open('common/media/photo.webp', 'rb'),
        'text': f'''

        <a href="https://proweb.uz/img/bonusMob.48c11c86.webp">&#8205;</a>

Qimmatbaho sovrinli tanlovlar har oy <b>PROWEB</b>
markazi o'quvchilari uchun o'tkaziladi!🎉

Tanlovlarda qatnashish uchun botimizga obuna bo'lishingiz kerak.

Tanlov shartlari ko'rsatilgan batafsil xabarlar barcha obunachilarga shaxsiy xabar orqali yuboriladi. Obunani
saqlab qolish uchun botni to'xtatmaslik yoki bloklamaligingiz kifoya.

Shuningdek, biz Instagram, Youtube, Telegram, Facebookdagi obunachilarimiz uchun qo'shimcha tanlovlar o'tkazamiz - obuna
bo'ling va bir vaqtning o'zida bir nechta tanlovlarda ishtirok eting.

Hammaga omad, har bir talabada g'alaba qozonish imkoniyati bor!🍀
'''},


    'base_course': f'''
Sizda umuman kompyuter bilimlari yo'q, lekin <b>PROWEB</b>da o'qishni xohlaysizmi? Bu bizning kompyuter asoslari kursimiz bilan mumkin.
Buning uchun "<b>Kompyuter asoslari kursiga yozilish</b> tugmasini bosish kifoya va o'qituvchimiz sizga hamma narsa haqida batafsil maslahat beradi."
<a href="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbOUYyx-etIXXSqfPAqohjX0LuKCUWjPWj9A&s">&#8205;</a>
''',


    
    'wishes': f'''
Sizga <b>PROWEB</b> markazida oq'ish yoqadimi va bu haqda ijtimoiy tarmoqlarimizda bo'lishish siz uchun qiyin emasmi? Bo'lmasam "<b>Sharhlar</b>
" havolasiga o'ting va taassurotlaringizni ta'riflang, biz sizga juda minnatdor bo'lamiz.

Agar siz mashg'ulot paytida qiyinchiliklarga duch kelsangiz yoki sizga biror narsa yoqmagan bo'lsa, ehtimol sizda taklif va istaklar bor bo'lsa?
Bo'lmasam "<b>Shikoyat va istaklar</b> havolasiga o'ting, hamma narsani batafsil tavsiflab bering va biz o'quv markazimizni yaxshilash uchun"
qolimizdan kelganini qilamiz.
''',

    'reply_btns': 
    
    {'main': [
        
        {'text': 'Bosh sahifaga ↩️', 'request_contact': None},
        {'text': "Русский язык 🇷🇺", 'request_contact': None},
        {'text': "Kontakt bilan ulashing", 'request_contact': True},

    ]},


    'inline_btns': 
    
    {
        'main': [
        
        {'text': 'Texnik yoram', 'url': 't.me/itsmylifestyle', 'callback_data': None},
        {'text': "Kovorking", 'url': 't.me/proweb_coworking', 'callback_data': None},
        {'text': "Tanlovlar🎉", 'url': None, "callback_data":'konkursi'},
        {'text': "Saytga tashrif buyurish", 'url': 'proweb.uz', 'callback_data': None},
        {'text': "Kompyuter asoslari", 'url': None, 'callback_data': 'base_course'},
        {'text': "Sharh qoldirish", 'url': None, 'callback_data': 'comment'},
        {'text': "O'qish qoidalari", 'url': 't.me/proweb_coworking', 'callback_data': None},

    ],
    
    'base_course': [{'text': 'Kompyuter asoslari kursiga yozilish', 'url': 't.me/proweb_basics', 'callback_data': None}],
    

    'wishes': [
            {'text': 'Sharhlar 😍', 'url': 'https://proweb.uz/uz/reviews/', 'callback_data': None},
            {'text': 'Shikoyat va istaklar 😔', 'url': 'https://proweb.uz/reviews/', 'callback_data': None},
            ],

    },
    

    },

}


