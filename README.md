# 開發環境建立說明

本專案使用FastAPI Framework, 根據以下步驟, 可以建立開發環境

1. 請先建立.env 環境變數檔, 並創建DB_CONN參數. DB_CONN 參數為 mysql 連線字串
2. 請參照Dockerfile 建立符合Python版本的虛擬環境
3. 本專案使用ORM First. Table 將會自動創建. 此前提下, 請先建立資料庫, Table會在此建立
4. 執行 uvicorn main:app --reload


# 部署說明(Google App Engine)

1. 請調整app.yaml DB_CONN 環境變數
2. 建立資料庫, 稍後Table會在此建立
3. 執行gcloud deploy app


# 執行Container

1. docker build . tag crawler
2. docker run crawler -d -p 8080:8080
