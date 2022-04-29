# 范例URL：
    'https://guorn.com/stock/rule/definition?id=402748.R.182851019003326

对应页面：
    https://guorn.com/stock/strategy?sid=402748.R.182851019003326



# Json
{"status": "ok", 

"data": 
{
    "category": "fund", 
    "saveas": false, 
    
    "current_tab": "back_test", 
    
    "name": "001_\u52a8\u91cf\u8f6e\u52a8\u7b56\u7565_\u884c\u4e1a_1", 
    
    
    "ranks": [{"asc": false, "industry": null, "id": "0.M.ETF\u6bcf\u65e5\u6307\u6807_N\u65e5\u6da8\u5e45.0#13", "weight": 1}], 

    "exclude_st": 0, 

    "visibility": 1, 
    
    "tabs": 
    {"back_test": {"count": "1", "backup_num": "2", "position_limit": 1, "end": "2020/09/01", "weight": "", "reference": "000300", "original_vol": false, "trading_strategy": {"hold_options": [], "buy_options": [], "sell_options": [{"id": "0.SM.\u6392\u540d\u540d\u6b21.0", "val": "20", "op": "ge"}]}, "price": "close", "ideal_position": 0.1, "period": 2, "position_bias": 0.3, "max_count": 15, "min_position": 0.01, "ideal_count": 10, "trade_cost": 0, "model": 0, "start": "2016/01/01", "always_tradable": 0, "hedge": false, "backup_fund": ""}, "screen": {"date": "2020/09/01", "period": "2", "original_vol": false}, 
    
    "rank": {"end": "2020/09/01", "reference": "000300", "bucket_count": "10", "period": 20, "start": "2016/01/01", "IC_bucket": false}
    
    }, 
    
    "pool": "402748.P.182850950685481",
    
    "filters": [{"type": "attr", "id": "0.A.\u57fa\u91d1\u7c7b\u522b.0", "val": [0, 1, 2, 4, 5], "op": "in"},
     {"industry": null, "type": "meas", "id": "402748.DI.182851550626604", "val": "1", "op": "eq"}, 
     {"industry": null, "type": "meas", "id": "0.M.ETF\u6bcf\u65e5\u6307\u6807_N\u65e5\u6da8\u5e45.0#13", "val": 0.005000000000000001, "op": "gt"}], 
     "target_shares": [], 
    
    "timing": 
        {
            "indicators": [], 
            "position": "0", 
            "threshold": ["-1", "-1"]
        }, 
    
    "id": "402748.R.182851019003326", 
    
    "strategy_source": 0, 
    
    "desc": ""
    }
}