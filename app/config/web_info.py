from enum import Enum


class TaiwanCompanyRanking(Enum):
    """
    台灣公司Rank網站 相關資訊
    """
    landing_page = 'https://rank.twincn.com/'
    company_summary = 'https://rank.twincn.com/item.aspx?no='
    company_detail = 'https://www.twincn.com/item.aspx?no='
    default_header = {
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'priority': 'u=0, i',
        'cookie': '_gid=GA1.2.2083970117.1720429370; ASP.NET_SessionId=lgktwrc5ojpra5qbea0lw4sp; __gads=ID=4f2d6c6a61dee307:T=1713767407:RT=1720447704:S=ALNI_MYnSrYGXC2QmofZoT-Z7kFh4Yv0tQ; __gpi=UID=00000df5b8206e5e:T=1713767407:RT=1720447704:S=ALNI_MaL63nxI1AiECIt8_eYSTAaG5gFZA; __eoi=ID=f49d7e5c08789701:T=1713767407:RT=1720447704:S=AA-AfjYNzBil9pHos1OoUWAdzuPa; _ga_BRKMV5VD1P=GS1.1.1720446280.5.1.1720447771.0.0.0; _ga=GA1.2.1629668842.1713767407; FCNEC=%5B%5B%22AKsRol_qa3nL_oV5gP6ncMOrVgQLhpT2xvCM6hU-4qy92_k-a8Ytw9wrthqwDTqdVg4CGFnx_AjWhEsaCPV-KSy-W4twjoBsKRIPyRuqOrciUI6CLOd7GCcxsNHAuNtPHTSfrRZmis1nP35OSytgm6EmCrqi75zzMQ%3D%3D%22%5D%5D; _ga_JJ8ZENTE7M=GS1.1.1720446270.10.1.1720447959.0.0.0'}
