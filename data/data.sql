USE fin_data_project;

CREATE TABLE s_and_p_stocks (
	Symbol VARCHAR(100) NOT NULL,
    Security VARCHAR(255) NOT NULL,
    GICS_Sector VARCHAR(255),
    GICS_Sub_Industry VARCHAR(255),
    Headquarters_Location VARCHAR(255),
    Date_Added DATE,
    CIK INT NOT NULL,
    Founded DATE,
    PRIMARY KEY (Symbol)
);

CREATE TABLE yfin_ticker_info (
	Ticker VARCHAR(100) NOT NULL,
    Beta INT NOT NULL,
    Recommendation_Score INT NOT NULL,
    PRIMARY KEY (Ticker)
);