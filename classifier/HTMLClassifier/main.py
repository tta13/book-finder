from HTMLclassifier import HTML_classifier

if __name__ == '__main__':
    clf = HTML_classifier()
    #rest = clf.preprocess_url('https://www.amazon.com.br/Disciplina-%C3%89-Liberdade-Manual-Campo/dp/6555204869?ref=dlx_67407_sh_dcl_img_0_40a1de71_dt_mese7_04,1')
    #print(rest)
    #clf.train_classifier()
    #clf.test_classifier()
    clf.predict_score(['2022-08-12_04.03.26.162585.html'])