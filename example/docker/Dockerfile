# Dockerfile
FROM ubuntu:latest

# 환경 변수 정의
ARG PASS=test123
# 패키지 목록 업데이트 및 필요한 패키지 설치
RUN apt-get update && \
    apt-get install -y openssh-server vim

# SSH 서비스 설정 (필요한 경우)
RUN mkdir /var/run/sshd
RUN echo root:$PASS | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH 포트 열기
EXPOSE 22

# SSH 서버 실행
CMD ["/usr/sbin/sshd", "-D"]
