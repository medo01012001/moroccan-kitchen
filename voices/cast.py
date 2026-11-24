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
]

def lines(c):
    _, _, _, _, _, opener, suf, thanks, wrong, angry = c
    out = [thanks, wrong, angry] + [f'{opener} {d}{suf}' for _, d in DISHES]
    return out

def script(c, lo=0, hi=None):
    return ' <long pause> <long pause> '.join(l + ('' if l.endswith('؟') else '.') for l in lines(c)[lo:hi])

if __name__ == '__main__':
    if sys.argv[1] == 'json':
        print(json.dumps([{'id':c[0],'face':c[1],'name':c[2],'opener':c[5],'suf':c[6]} for c in CAST], ensure_ascii=False))
    else:
        c = CAST[int(sys.argv[1])]
        lo = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        hi = int(sys.argv[3]) if len(sys.argv) > 3 else None
        print(c[3]); print(BASE.format(who=c[4])); print(script(c, lo, hi))
