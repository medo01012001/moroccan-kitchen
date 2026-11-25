# Voice cast for the customers. Run: python cast.py <index>  -> prints style + script
import sys, json

DISHES = [
 ('atay','أتاي بالنعناع'),('bissara','بيصارة'),('bqoula','بقولة'),('fishtajine','طاجين الحوت'),
 ('karantita','كرانطيطة'),('berkoukech','بركوكش'),('mechoui','المشوي'),('pastilla','بسطيلة'),
 ('mrouzia','المروزية'),('harira','حريرة'),('prunes','طاجين البرقوق'),('sellou','سلو'),('seffa','سفة'),
 ('couscous','كسكس بسبع خضاري'),('kefta','طاجين الكفتة'),('babbouche','ببوش'),('rfissa','رفيسة'),
 ('chicken','طاجين الدجاج'),('orange','عصير الليمون'),('tanjia','طنجية'),('sardine','سردين معمر'),
 ('msemen','مسمن بالعسل'),('medfouna','مدفونة'),('datemilk','حليب بالتمر'),('vegtajine','طاجين الخضرة'),
 ('amlou','أملو'),('asida','عصيدة'),('grilled','حوت مشوي'),('sahtea','أتاي صحراوي'),('camel','طاجين لحم الجمل'),
 ('camelmilk','حليب النوق بالتمر'),('malfouf','ملفوف'),('zrig','زريك'),('riz','روز باللحم'),
 ('oysters','محار الداخلة'),('octopus','طاجين الأخطبوط'),('marrou','مارو بالحوت'),
]

BASE = ("Speak in Moroccan Darija (Moroccan Arabic dialect, Casablanca accent), not standard Arabic. "
        "{who} Natural pace. Leave a clear silence between sentences.")

# id, face, name, voice, persona, opener (before dish), suffix, thanks, wrong, angry
CAST = [
 ('alal','👴','با علال','Algenib','An old Moroccan grandfather, warm and a little raspy, ordering food in a busy restaurant.',
  'الله يرحم الوالدين بغيت','', 'الله يعطيك الصحة بنينة بزاف','لا لا ماشي هادشي اللي طلبت','تعطلت بزاف أنا ماشي بسلامة'),
 ('fatna','👵','مي فاطنة','Gacrux','An old Moroccan grandmother, sweet and motherly, ordering food in a busy restaurant.',
  'الله يخليك بغيت','', 'الله يرضي عليك ويسهل عليك','آش هادشي؟ ماشي هادا اللي طلبت','واش هادي ساعة وأنا كنتسنى؟ مشيت'),
 ('mohamed','👨','سي محمد','Achird','A friendly Moroccan man in his forties, polite, ordering food in a busy restaurant.',
  'السلام عليكم عافاك بغيت','', 'شكرا بزاف الله يعطيك الصحة','سمح ليا هادشي ماشي ديالي','ما بقيتش نقدر نتسنى سلام'),
 ('zahra','🧕','لالة زهرة','Sulafat','A warm Moroccan woman in her thirties, cheerful, ordering food in a busy restaurant.',
  'صباح الخير بغيت','', 'تبارك الله عليك بنين بزاف','أويلي ماشي هادشي اللي طلبت','صافي مشيت ما عنديش الوقت'),
 ('omar','👳‍♂️','الحاج عمر','Charon','A wise, calm, deep-voiced elderly Moroccan Hajj, respectful, ordering food in a restaurant.',
  'بسم الله جيب ليا','', 'الله يجازيك بخير','لا ألحبيب هادشي ماشي ديالي','حشومة هادشي تعطلتو بزاف'),
 ('hamid','👦','حميد','Zeno','A cheeky, excited ten-year-old Moroccan boy with a young high voice, ordering food in a restaurant.',
  'عافاك بغيت','', 'واو بنين شكرا','ماشي هادي اللي بغيت','جوعان بزاف غادي نمشي عند ماما'),
 ('salma','👧','سلمى','Leda','A sweet, happy eight-year-old Moroccan girl with a small high voice, ordering food in a restaurant.',
  'عافاك عطيني','', 'ميرسي بزاف بنين','لا ماشي هادي','أوف تعطلتو بزاف غادي نمشي'),
 ('arbi','🧔','سي العربي','Fenrir','A loud, hungry, funny Moroccan man, very expressive, ordering food in a busy restaurant.',
  'جوعان بزاف بغيت','', 'هادي هي الماكلة ولا بلاش','شنو هادا؟ ماشي هادا اللي طلبت','باراكا من التسنية مشيت'),
 ('khadija','👩','خديجة','Aoede','A young Moroccan woman, relaxed and kind, asking for food in a restaurant.',
  'واش كاين','؟', 'شكرا بزاف الله يحفظك','سمح ليا هادي ماشي ديالي','صافي ما غاديش نتسنى كثر'),
 ('yassine','🧑‍🎓','ياسين','Puck','A Moroccan university student in a hurry, upbeat and fast-talking, ordering food.',
  'دغيا عافاك عندي القراية بغيت','', 'شكرا بزاف واعر','ماشي هادي اللي طلبت','فاتني الكور بسبابكم'),
 ('police','👮','الشرطي','Orus','A serious, firm Moroccan policeman on his lunch break, ordering food in a restaurant.',
  'السلام بغيت','', 'مزيان شكرا','هادشي غالط ماشي هادا اللي طلبت','تعطلتو بزاف مشيت'),
 ('farmer','🧑‍🌾','عمي الفلاح','Umbriel','A simple, kind Moroccan farmer from the countryside with a rural accent, ordering food.',
  'الله يعاونك بغيت','', 'الله يبارك فيك بحال ماكلة البلاد','لا لا ماشي هادي اللي طلبت','خليت البهايم بوحدهم مشيت'),
 # VIP guests (appear in any region)
 ('vip_foot','⚽','لاعب المنتخب','Alnilam','A famous young Moroccan national-team football player, energetic and confident, in a hurry to get to training, ordering food.',
  'أنا زْرْبان عندي التدريب بغيت','', 'واعر غادي نقول لصحابي كاملين','لا لا خويا ماشي هادشي اللي طلبت','مشيت وغادي نكتب عليكم فالأنستا'),
 ('vip_singer','🎤','المغنية المشهورة','Laomedeia','A famous Moroccan pop singer, glamorous, lively and a bit diva, in a hurry before her concert, ordering food.',
  'عافاك دغيا عندي سهرة بغيت','', 'واعر غادي نقول لصحاباتي كاملين','أويلي ماشي هادشي اللي طلبت','مشيت وغادي نكتب عليكم فالأنستا'),
 ('vip_actor','🎬','الممثل ديال المسلسل','Iapetus','A famous Moroccan TV-series actor, dramatic and theatrical, the cameras are waiting for him, ordering food.',
  'الكاميرات كيتسناوني بغيت','', 'واعر غادي نقول لصحابي كاملين','لا لا ماشي هادا اللي طلبت','مشيت وغادي نكتب عليكم فالأنستا'),
 ('vip_chaabi','🕺','الفنان الشعبي','Sadachbia','A famous, joyful Moroccan chaabi folk singer, loud and funny, full of life, ordering food.',
  'آ الشريف بغيت','', 'واعر غادي نقول لصحابي كاملين','آ الشريف ماشي هادشي اللي طلبت','مشيت وغادي نكتب عليكم فالأنستا'),
]

# the chef's mother: (clip name, text)
MAMA_VOICE = 'Vindemiatrix'
MAMA_WHO = 'A loving but bossy old Moroccan mother visiting the restaurant kitchen of her child, expressive and funny.'
MAMA = [
 ('enter_m','السلام ولدي! شنو كتطيب؟'),
 ('enter_f','السلام بنتي! شنو كتطيبي؟'),
 ('finish','ماشي هاكا كيطيبو! عطيني نوريك'),
 ('clean_m','آش هاد الدخان؟ جيب شي حاجة نقي ليك هاد الروينة'),
 ('clean_f','آش هاد الدخان؟ جيبي شي حاجة نقي ليك هاد الروينة'),
 ('gift_m','جبت ليك شوية السلعة من الدار، ما تقولش ما عندكش'),
 ('gift_f','جبت ليك شوية السلعة من الدار، ما تقوليش ما عندكش'),
 ('salt_m','زدت ليك شوية الملحة، ما تقول والو'),
 ('salt_f','زدت ليك شوية الملحة، ما تقولي والو'),
 ('tip1_m','ولدي، عطي اللول للكليان اللي قرب يسالي ليه الصبر'),
 ('tip1_f','بنتي، عطيي اللول للكليان اللي قرب يسالي ليه الصبر'),
 ('tip2','ما تخليش الماكلة فالكانون، راه كتحرق'),
 ('tip3_m','سير للسوق قبل ما تقاضا السلعة'),
 ('tip3_f','سيري للسوق قبل ما تقاضا السلعة'),
 ('tip4_m','الله يرضي عليك أولدي، كمل هاكا'),
 ('tip4_f','الله يرضي عليك أبنتي، كملي هاكا'),
 ('tip5','فزماني كنا كنطيبو للعرس كامل بكانون واحد'),
]

def lines(c):
    _, _, _, _, _, opener, suf, thanks, wrong, angry = c
    out = [thanks, wrong, angry] + [f'{opener} {d}{suf}' for _, d in DISHES]
    return out

def script(c, lo=0, hi=None):
    return ' <long pause> <long pause> '.join(l + ('' if l.endswith('؟') else '.') for l in lines(c)[lo:hi])

if __name__ == '__main__':
    if sys.argv[1] == 'mama':
        print(MAMA_VOICE); print(BASE.format(who=MAMA_WHO))
        print(' <long pause> <long pause> '.join(t + ('' if t.endswith('؟') else '.') for _, t in MAMA))
        sys.exit()
    if sys.argv[1] == 'json':
        print(json.dumps([{'id':c[0],'face':c[1],'name':c[2],'opener':c[5],'suf':c[6]} for c in CAST], ensure_ascii=False))
    else:
        c = CAST[int(sys.argv[1])]
        lo = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        hi = int(sys.argv[3]) if len(sys.argv) > 3 else None
        print(c[3]); print(BASE.format(who=c[4])); print(script(c, lo, hi))
