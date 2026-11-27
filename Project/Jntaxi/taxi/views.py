from django.shortcuts import render, HttpResponse, redirect
import pandas as pd
import json  # 必须导入 json
import webbrowser


# Create your views here.
def map_demo(request):
    return render(request, 'map_demo.html')


def login(request):
    return render(request, 'index.html')


def UTC(requset):
    return redirect('https://www.matools.com/timestamp?embed')


def map(request):
    return render(request, "map.html")


# ================= 按时间查询 =================
def relay2(request):
    star = request.GET.get('StartTime')
    end = request.GET.get('EndTime')

    # 容错处理：如果没有传参数直接返回空
    if not star or not end:
        return render(request, 'View.html', {"aa": json.dumps([])})

    StartTime = int(star)
    EndTime = int(end)

    data = pd.read_csv(r'./static/data/0912_view.csv', encoding='utf-8')
    dta = data[(data['UTC'] >= StartTime) & (data['UTC'] <= EndTime)]

    car = []
    for i in range(0, len(dta)):
        # 强制转为 float，防止 numpy 的 float64 导致 json 序列化失败
        car.append({
            'lat': float(dta.iloc[i, 2]),
            'lng': float(dta.iloc[i, 3]),
            'name': str(dta.iloc[i, 0])
        })

    # print(f"传给前端aa数组长度：{len(car)}")

    # 关键：使用 json.dumps 转换为标准 JSON 字符串，并指定 ensure_ascii=False 防止中文乱码
    return render(request, 'View.html', {"aa": json.dumps(car, ensure_ascii=False)})


# ================= 按车辆查询 =================
def relay3(request):
    StartTime = int(request.GET.get('StartTime'))
    EndTime = int(request.GET.get('EndTime'))

    # 前端传过来的车牌号可能是字符串，先拿过来
    car_id_str = request.GET.get('CarId')

    data = pd.read_csv(r'./static/data/0912_view.csv', encoding='utf-8')

    # 容错：尝试将CSV里的车牌列转为字符串再比对，防止 int 和 str 匹配不上
    # 注意核对你的 CSV 表头到底是 CarId 还是 CarID
    if 'CarID' in data.columns:
        data = data[data['CarID'].astype(str) == str(car_id_str)]
    elif 'CarId' in data.columns:
        data = data[data['CarId'].astype(str) == str(car_id_str)]

    dta = data[(data['UTC'] >= StartTime) & (data['UTC'] <= EndTime)]

    car = []
    for i in range(0, len(dta)):
        car.append({
            'lat': float(dta.iloc[i, 2]),
            'lng': float(dta.iloc[i, 3]),
            'name': str(dta.iloc[i, 0]),
            'UTC': int(dta.iloc[i, 1])
        })

    return render(request, 'Dynamic.html', {"aa": json.dumps(car, ensure_ascii=False)})

def fx(request):
    webbrowser.open("http://localhost:8000/relay5")
    return render(request,'map.html')

def fx1(request):
    return render(request,'index_fx.html')