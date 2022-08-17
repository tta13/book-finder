from url_classifier import url_classifier

if __name__ == '__main__':
    clf = url_classifier()
    #rest = clf.preprocess_url('https://www.amazon.com.br/Disciplina-%C3%89-Liberdade-Manual-Campo/dp/6555204869?ref=dlx_67407_sh_dcl_img_0_40a1de71_dt_mese7_04,1')
    #print(rest)
    #clf.train_classifier()
    #clf.test_classifier()
    clf.predict_score('https://www.amazon.com.br/Disciplina-%C3%89-Liberdade-Manual-Campo/dp/6555204869?ref=dlx_67407_sh_dcl_img_0_40a1de71_dt_mese7_04,1')