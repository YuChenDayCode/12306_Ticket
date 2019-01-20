# Ticket
## 12306

步骤
### 1.查询
https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2019-02-14&leftTicketDTO.from_station=CQW&leftTicketDTO.to_station=TVW&purpose_codes=ADULT
```
参数：{
        leftTicketDTO.train_date:2019-02-14  #购票日期
        leftTicketDTO.from_station:CQW #起点站
        leftTicketDTO.to_station:TVW #终点站
        purpose_codes:ADULT #购票类型，ADULT代表单程
      }
返回：{"data":{"flag":"1","map":{"CUW":"重庆北","CXW":"重庆西","TVW":"潼南"},"result":["|列车运行图调整,暂停发售|77000D51030J|D5103|CXW|ICW|CXW|TVW|24:00|24:00|99:59|IS_TIME_NOT_BUY||20190214||W3|01|03|0|1|||||||||||||||||0|0|null","|列车运行图调整,暂停发售|77000D51170A|D5117|CUW|NIW|CUW|TVW|24:00|24:00|99:59|IS_TIME_NOT_BUY||20190214||W2|01|03|0|1|||||||||||||||||0|0|null","IQEEzf7ymvboXyZSxb%2Bvno%2FvYNEZbmuqDINQp%2Bmnh3k4f0fECt06bHNQPKk4Hlpp8k%2FEY%2FHY1hMb%0Aua7x0jZi61wrCfaoT%2FPBfZMLd4iBVRZurosYHAz0E191H6A5Imnmwng39zx10jq6Bj5eBTTWbH4U%0Ag5a1RfO85IpYBCUAfwSajgMxulbU63F6m2rH%2Bn3QV2djAIrKzIDYwjfdFAuLAfzMa5Sb0cV3nEG7%0AnW43VHcCPF9qB%2BvHUSuHaQcbaHdYztBgPpKcWEXeSXZ0Hekt8%2BIORs8NXs%2FMiGi%2FLkbi5NdZYb%2BJ%0Ax36wYA%3D%3D|预订|710000K1420H|K143|NNZ|CDW|CXW|TVW|09:18|10:36|01:18|Y|t47JENLelAwrUH8jO7aObclgoEFHNBYIMu9USdXqyieI0PymUpkzmENrhno%3D|20190213|3|Z1|11|12|0|0||||2|||有||有|16|||||10401030|1413|0|0|null","MUyH%2FHTEfnPsZwsT%2B2JzqnO21xQ5sGp0nnfSH52Dxg82ZvrybT7nChBhBxb3TsvMjtJyUJx89uNQ%0AMCrH9ekzbik0zw54JI4FG7uavZBLFJwJFKM6jXIhI6akPir9cafU%2BO07Fq2oHvjihljCWeydEtMq%0AHltj9Cl6HqKGR9xxZS1UsSAWqyjFBxPFLPFkPjn1LwFH%2FnvW1li%2FMEDeRugFkjsdIzBNPnrhDB3I%0A%2Bi022Xdvfv8XW3YA0vrhyYKwZU%2FGAR52EgfaJAMKGomYC%2F6HFjCas%2BCl8big1Vkw%2FuIAObayl7Is%0AtwecSA%3D%3D|预订|710000K8720H|K873|ZJZ|............."]},"httpstatus":200,"messages":"","status":true}
```

### 2.https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest # 提交下单请求   
```
参数：{
        secretStr:NwCfMpWhQYGrv9zKy/E2bJHhqOoVHXTgo5hTboBBIe/Kzro2zxrnAiA4x1lswwh5upe5V31vZwXQuv7gxy...  # 这个参数是第一步查询的第一个参数，那趟车可买票的时候才会有这个参数
        train_date:2019-02-14  # 发车日期
        back_train_date:2019-01-20 # 返程日期（不是往返票不用管他）
        tour_flag:dc # 单程
        purpose_codes:ADULT # 普通票
        query_from_station_name:重庆 #起点站
        query_to_station_name:潼南 # 终点站
        undefined:  # 为空的参数
      }
返回：{"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":"N","messages":[],"validateMessages":{}}
```

### https://kyfw.12306.cn/otn/confirmPassenger/initDc #获取一堆参数 后面的请求需要用到   
```
参数：{
        _json_att：''
      }
返回的是一个页面，需要用正则去取数据
```

### 3.https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs # 获取购票人信息 (乘车人信息)  
```
参数：{
        _json_att:'',
        REPEAT_SUBMIT_TOKEN:1e4811cbf86e722b50c7cb4293d1969c
      }
返回：{"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":{"notify_for_gat":"","isExist":true,"exMsg":"","two_isOpenClick":["93","95","97","99"],"other_isOpenClick":["91","93","98","99","95","97"],"normal_passengers":[{"code":"2","passenger_name":"XX","sex_code":"M","sex_name":"男","born_date":"199....","country_code":"CN","passenger_id_type_code":"1","passenger_id_type_name":"中国居民身份证","passenger_id_no":"500223....","passenger_type":"1","passenger_flag":"0","passenger_type_name":"成人","mobile_no":"13...","phone_no":"","email":"...@qq.com","address":"","postalcode":"","first_letter":"CZ","recordCount":"7","total_times":"99","index_id":"0","gat_born_date":"","gat_valid_date_start":"","gat_valid_date_end":"","gat_version":""},{"code":"1","passenger_name":"XX","sex_code":"M","sex_name":"男","born_date":"2016-02-14 00:00:00","country_code":"CN","passenger_id_type_code":"1","passenger_id_type_name":"中国居民身份证","passenger_id_no":"500230....","passenger_type":"1","passenger_flag":"0","passenger_type_name":"成人","mobile_no":"","phone_no":"","email":"","address":"","postalcode":"","first_letter":"AJ","recordCount":"7","total_times":"99","index_id":"1","gat_born_date":"","gat_valid_date_start":"","gat_valid_date_end":"","gat_version":""},{"code":"4","passenger_name":"XXX","sex_code":"F","sex_name":"女","born_date":"1900-01-01 00:00:00","country_code":"CN","passenger_id_type_code":"1","passenger_id_type_name":"中国居民身份证","passenger_id_no":"511602........","passenger_type":"1","passenger_flag":"0","passenger_type_name":"成人","mobile_no":"15.....","phone_no":"","email":"","address":"","postalcode":"","first_letter":"DYM","recordCount":"7","total_times":"99","index_id":"3","gat_born_date":"","gat_valid_date_start":"","gat_valid_date_end":"","gat_version":""}]},"messages":[],"validateMessages":{}}
```

 
### 4.https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo # 检查订单信息 (是否能购票，是否有未支付的订单）   
```
参数:{
    cancel_flag:2
    bed_level_order_num:000000000000000000000000000000
    passengerTicketStr:O,0,1,陈震,1,500223199304258858,13220367145,N
    oldPassengerStr:陈震,1,500223199304258858,1_
    tour_flag:dc
    randCode:''
    whatsSelect:1
    _json_att:''
    REPEAT_SUBMIT_TOKEN:1e4811cbf86e722b50c7cb4293d1969c
}
返回:{"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":{"ifShowPassCode":"N","canChooseBeds":"N","canChooseSeats":"Y","choose_Seats":"OM","isCanChooseMid":"N","ifShowPassCodeTime":"1","submitStatus":true,"smokeStr":""},"messages":[],"validateMessages":{}}
```

### 5.https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount # 获取余票，与排队人数
```
参数{
        train_date:Thu+Feb+14+2019+00:00:00+GMT+0800+(中国标准时间) #购票时间格式化出来的
        train_no:77000D514708 # 车次
        stationTrainCode:D5147 #班次
        seatType:O # O代表二等座，这儿有个固定字典的类型
        fromStationTelecode:CUW #起点站简码
        toStationTelecode:TVW #终点站简码
        leftTicket:CLy0iYHVYp2Mctmf3%2FRbBmuCCUGyeyU8JF%2Bjolnv%2FfplIrD2 #第三步获取的
        purpose_codes:00  #第三步获取的
        train_location:W2 #第三步获取的
        _json_att:为空
        REPEAT_SUBMIT_TOKEN:1e4811cbf86e722b50c7cb4293d1969c #第三步获取的
}
返回:{"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":{"count":"0","ticket":"463,85","op_2":"false","countT":"0","op_1":"false"},"messages":[],"validateMessages":{}}
```

### 6.https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue #选座提交  
```
参数：{
        passengerTicketStr:O,0,1,XX,1,500....,132.....,N   # 拼接的购票人信息
        oldPassengerStr:XX,1,5002....,1_     # 拼接的购票人信息
        randCode:'' #空数据
        purpose_codes:00   # 第三步获取
        key_check_isChange:5EAB44C37C430901F5D2AA18462DD31BDADFE7DE17048A36906509CD   # 第三步获取
        leftTicketStr:Imh2yxCys%2Fo%2FhDX%2B3ZZOYgnkoNLrsZz6OFEYF5oGBrFRIB2p  # 第三步获取
        train_location:W2  # 第三步获取
        choose_seats:1D #选的座位，没有的话他会帮你随机选。。
        seatDetailType:000   # 固定
        whatsSelect:1  # 固定
        roomType:00   # 固定
        dwAll:N   # 固定
        _json_att:''  #空
        REPEAT_SUBMIT_TOKEN:a8dc2ed1a814b3067cfc32550c17e0ed   # 第三步获取
}
返回:{"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":{"submitStatus":true},"messages":[],"validateMessages":{}}
```

### 7.https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random=1547780170175&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN=a8dc2ed1a814b3067cfc32550c17e0ed # 排队   
```
参数:{
        random	1547780170175 #秒级时间戳
        tourFlag:dc # 固定的 普通票
        _json_att:'' 
        REPEAT_SUBMIT_TOKEN:a8dc2ed1a814b3067cfc32550c17e0ed #第三步获取
}
返回：{"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":{"queryOrderWaitTimeStatus":true,"count":0,"waitTime":-1,"requestId":6491860556856379439,"waitCount":0,"tourFlag":"dc","orderId":"E702546392"},"messages":[],"validateMessages":{}}
```

### 8.https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue # 确定下单成功   
```
参数{
        orderSequence_no:E702546390  #上一步返回的订单id
        _json_att:'' #空
        REPEAT_SUBMIT_TOKEN:a8dc2ed1a814b3067cfc32550c17e0ed #第三步的
}
返回:{"validateMessagesShowId":"_validatorMessage","status":true,"httpstatus":200,"data":{"submitStatus":true},"messages":[],"validateMessages":{}}
```
