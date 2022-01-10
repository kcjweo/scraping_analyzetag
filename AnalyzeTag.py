
def main():

    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException


    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Chrome(executable_path='/Users/anatanonamae/Desktop/Tool/chromedriver', chrome_options=options)

    browser.implicitly_wait(3)

    # 1ページ目にアクセス
    PAGE = 1
    InitURL= "https://teratail.com/search?tab=active&page=" + str(PAGE) + "&q=is%3Anot-answered"
    browser.get(InitURL)
    print("1ページ目にアクセスしました")

    #各ページで情報収集    
    TAG_DIC={}    
    while True:
        A_TAG = browser.find_elements_by_tag_name("a")#a タグを収集

        taglist=[]
        for TAG in A_TAG :
            HREF = TAG.get_attribute('href') #hrefを収集

            if "tags" in str(HREF):#tagが含まれるhrefを収集
                if not TAG.text:
                    continue                        
                else:
                     taglist.append(TAG.text)

        for tag in taglist:
            if tag in TAG_DIC:
                 TAG_DIC[tag] += 1
            else:
                TAG_DIC[tag] = 1

        NEXT_XPATH = browser.find_elements_by_xpath("//*[@id=\"mainContainer\"]/div[4]/div/p/a/span[contains(text(),\'次のページ\')]")

        if NEXT_XPATH:#次へがある場合はPAGEを加算
            PAGE += 1

        else:
            print("Got tags at last page.")#なければ終わり
            break

        browser.get(URL)#次のページへ移動
        WebDriverWait(browser, 2).until(EC.presence_of_all_elements_located)
        print(browser.current_url)
        if browser.title == "ページが見つかりません":
            print("Got tags at last page.")#次のページへがエラーとなった場合は終わり
            break

    # 後処理：Dataframeの作成
    df = pd.DataFrame([TAG_DIC.keys(),TAG_DIC.values()],index=None).T#Dataframeへ変換
    df.rename(columns={0:"Tag",1:"Count"},inplace =True)#列名を変更
    df.sort_values(by=['Count'],ascending=False,inplace =True)#多い順でソートする
    df.reset_index(drop=True,inplace=True)#indexを振り直す

    print(df)

if __name__ == "__main__":
    main()
