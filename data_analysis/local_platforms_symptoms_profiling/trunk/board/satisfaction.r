.skip.db = T
source('conf.r')

source('satisfaction-survey.r')

share.lib('stats')
share.lib('output')

i18n = function(x) { x }

r = read.csv2('satisfaction.csv', header=T)

init.output(my.path(''), 'satisfaction', type="html", opts=list(inline.css=T))

desc = function(data, question) {
  out( freq( as.labels(data[,question],question)), title=question_title(question)) 
}

for(question in survey.xml$questions) {
  if(question$type == "single-choice") {
    desc(r, question$dataname)
  }
  if(question$type == "multiple-choice") {
    v = names.glob(r, paste(question$dataname,"_*",sep=""))
    d = r[,v]
    n = sapply(v, question_title)
    names(d) <- n
    out( multiple.freq(d), title=question$title)
  }
}

out(summary(r$timestart/1000), title="Temps de réponse au questionnaire (secondes)")

close.output()

aliases = list(
  #Q0="",
  Q1="participe",
  Q1bis="frequency",
  Q2_1,
  Q2_2,
  Q2_3,
  Q2_4,
  Q2_5,
  Q2_6,
  Q2_7,
  Q2_8,
  Q2_9,
  Q2_10,
  Q2bis,
  Q3="talk.people",
  Q4="social.net",
  Q4bis="social.net.feature",
  Q5="intake.filltime",
  Q5bis="intake.toolong",
  Q6="weekly.filltime",
  Q6bis="weekly.toolong",
  Q8="survey.during.season",
  Q9="survey.outside.season"
  Q10="newsletter.read",
  Q11_1="newsletter.interesting",
  Q11_2"newsletter.not.interesting",
  Q11_3="newsletter.too.short",
  Q11_4="newsletter.too.long",
  Q11_5="newsletter.good.length",
  Q12="newsletter.frequency",
  Q13_1,
  Q13_2,
  Q13_3,
  Q13_4,
  Q13_5,
  Q13_6,
  Q13_7,
  Q13bis,
  Q14,
  Q15,
  Q16,
  Q17,
  Q18,
  Q19_1,
  Q19_2,
  Q19_3,
  Q19_4,
  Q19_5,
  Q19_6,
  Q19_7,
  Q19_8,
  Q20,
  Q21_1,
  Q21_2,
  Q21_3,
  Q21_4,
  Q21_5,
  Q21_6,
  Q21_7,
  Q21bis,
  Q22,
  Q22bis,
  Q23,
  subsidiaire,
  Q24,
  Q25_multi_row1_col1,
  Q25_multi_row2_col1,
  Q25_multi_row3_col1,
  Q25_multi_row4_col1,
  Q25_multi_row5_col1,
  Q25_multi_row6_col1,
  Q25_multi_row7_col1,
  Q25_multi_row8_col1,
  Q25_multi_row9_col1,
  Q25_multi_row10_col1,
  Q25_multi_row11_col1,
  Q25_multi_row12_col1,
  Q25_multi_row13_col1,
  Q25_multi_row14_col1,
  Q25_multi_row15_col1,
  Q25_multi_row16_col1,
  Q25_multi_row17_col1,
  Q25_multi_row18_col1,
  Q25_multi_row19_col1,
  Q25_multi_row20_col1,
  Q26_multi_row1_col1,
  Q26_multi_row2_col1,
  Q26_multi_row3_col1,
  Q26_multi_row4_col1,
  Q26_multi_row5_col1,
  Q26_multi_row6_col1

 