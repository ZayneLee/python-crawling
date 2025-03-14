import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

def send_email_alert(subject, message):
    sender = "openapierrors@gmail.com"
    receivers = ["jhoh@ezfarm.co.kr", "sdlee@ezfarm.co.kr", "smhong@ezfarm.co.kr", "sybaek@ezfarm.co.kr", "bchan@ezfarm.co.kr"]
    # HTML 형식 이메일 전송
    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(receivers)
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, "gkniypenrsheqtvc")  # 실제 앱 비밀번호를 입력하세요.
            server.sendmail(sender, receivers, msg.as_string())
        print("이메일 알림 전송 완료")
    except Exception as e:
        print("이메일 전송 실패:", e)

# 오늘 날짜를 YYYYMMDD 형식으로 구함
today = datetime.today().strftime("%Y%m%d")

# URL의 bgnde와 endde 파라미터에 오늘 날짜를 동적으로 삽입
url = f"http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/abandonmentPublic?bgnde={today}&endde={today}"
print("호출 URL:", url)

try:
    response = requests.get(url)
    response.raise_for_status()  # 요청 실패 시 예외 발생
    xml_data = response.text

    # BeautifulSoup을 사용하여 XML 파싱
    soup = BeautifulSoup(xml_data, "xml")
    total_count_element = soup.find("totalCount")
    
    if total_count_element is not None:
        total_count = int(total_count_element.text)
        if total_count == 0:
            print("데이터 조회 실패: 데이터가 없습니다.")
            failure_message = f"""
            <html>
              <body style="font-family: Arial, sans-serif; background-color: #f2f2f2; padding: 20px;">
                <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; border: 1px solid #ccc;">
                  <h2 style="color: #d9534f;">[공공데이터 포털] 데이터 조회 실패</h2>
                  <p>안녕하세요,</p>
                  <p>{today} 기준 외부 DB에 <strong>데이터가 존재하지 않습니다</strong>.</p>
                  <p>확인 부탁드립니다.</p>
                  <hr>
                  <p style="font-size: 0.9em; color: #888;">This is an automated message.</p>
                </div>
              </body>
            </html>
            """
            send_email_alert("데이터 조회 실패", failure_message)
        else:
            print(f"데이터 조회 성공: 총 {total_count} 건의 데이터가 조회되었습니다.")
            success_message = f"""
            <html>
              <body style="font-family: Arial, sans-serif; background-color: #f2f2f2; padding: 20px;">
                <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; border: 1px solid #ccc;">
                  <h2 style="color: #5cb85c;">[공공데이터 포털] 데이터 조회 성공</h2>
                  <p>안녕하세요,</p>
                  <p>{today} 기준 총 <strong>{total_count}</strong> 건의 데이터가 조회되었습니다.</p>
                  <hr>
                  <p style="font-size: 0.9em; color: #888;">This is an automated message.</p>
                </div>
              </body>
            </html>
            """
            send_email_alert("데이터 조회 성공", success_message)
    else:
        print("totalCount 태그를 찾을 수 없습니다.")
        error_message = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f2f2f2; padding: 20px;">
            <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; border: 1px solid #ccc;">
              <h2 style="color: #f0ad4e;">[공공데이터 포털] 데이터 조회 오류</h2>
              <p>안녕하세요,</p>
              <p>{today} 기준 totalCount 태그를 찾을 수 없습니다.</p>
              <hr>
              <p style="font-size: 0.9em; color: #888;">This is an automated message.</p>
            </div>
          </body>
        </html>
        """
        send_email_alert("데이터 조회 오류", error_message)
        
except Exception as e:
    print("오류 발생:", e)
    exception_message = f"""
    <html>
      <body style="font-family: Arial, sans-serif; background-color: #f2f2f2; padding: 20px;">
        <div style="background-color: #ffffff; padding: 20px; border-radius: 5px; border: 1px solid #ccc;">
          <h2 style="color: #d9534f;">[공공데이터 포털] 데이터 조회 오류</h2>
          <p>안녕하세요,</p>
          <p>데이터 조회 도중 오류가 발생했습니다.</p>
          <p><strong>오류 내용:</strong> {e}</p>
          <hr>
          <p style="font-size: 0.9em; color: #888;">This is an automated message.</p>
        </div>
      </body>
    </html>
    """
    send_email_alert("데이터 조회 오류", exception_message)
