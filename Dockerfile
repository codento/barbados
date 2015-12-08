FROM codento/supervisord

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=en_US.UTF-8

RUN apt-get install -y postgresql-server-dev-9.4

RUN mkdir -p /var/run/{{ project_name }}/ /var/log/uwsgi/ /root/.ssh/

ADD docker-assets/known_hosts /root/.ssh/known_hosts
ADD docker-assets/ssh_config /root/.ssh/config
ADD docker-assets/github_deployment_rsa /root/.ssh/id_rsa

ADD requirements.txt /opt/webapps/requirements.txt

RUN pip3 install -r /opt/webapps/requirements.txt

RUN groupadd -g 8000 {{ project_name }}
RUN useradd -g 8000 -u 8000 -m -k /etc/skel -d /opt/webapps/ -s /bin/balse {{ project_name }}

ADD docker-assets/uwsgi.ini /etc/uwsgi/uwsgi.ini
ADD docker-assets/supervisor_project.conf /etc/supervisor/conf.d/{{ project_name }}.conf

RUN chown -R 8000:8000 /var/run/{{ project_name }}/
RUN chown -R 8000:8000 /var/log/uwsgi/

RUN touch /etc/uwsgi/reload

EXPOSE 8000

CMD ["sh", "-c", "service supervisor restart"]

