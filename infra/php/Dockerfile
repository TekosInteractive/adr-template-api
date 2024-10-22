FROM php:8.2.2-fpm-bullseye AS php822fpm

ENV PHP_VERSION=php8.2

ARG XDEBUG_IDKEY
ARG XDEBUG_PORT
ARG XDEBUG_HOST
ARG XDEBUG_TRIGGERVALUE
ARG MAIL_PORT
ARG MAIL_HOST
ARG PHP_PORT
ARG APP_PATH
ARG USER_ID
ARG GROUP_ID

# COPY ./php.ini $PHP_INI_DIR/

# Copy composer.lock and composer.json
# COPY ./api/composer.lock ./api/composer.json /var/www/

# Set working directory
WORKDIR $APP_PATH

RUN apt-get update && apt-get -y install lsb-release apt-transport-https ca-certificates wget pkg-config apt-utils
RUN wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg
RUN echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | tee /etc/apt/sources.list.d/php.list

RUN apt-get update && apt-get install -y \
  libfreetype6-dev \
  libjpeg62-turbo-dev \
  libpng-dev \
  libicu-dev \
  libcurl4-openssl-dev \
  openssl \
  libxml2-dev \
  libzip-dev \
  libonig-dev\
  && docker-php-ext-configure gd --with-freetype --with-jpeg \
  && docker-php-ext-install -j$(nproc) gd intl bcmath curl xml zip mbstring mysqli iconv pdo_mysql \
  && apt-get purge -y libfreetype6-dev libpng-dev libjpeg-dev libicu-dev

# install xdebug
RUN pecl install xdebug
RUN docker-php-ext-enable xdebug

# Prevent error in nginx error.log
RUN touch /var/log/xdebug_remote.log && chmod 777 /var/log/xdebug_remote.log

#RUN echo "zend_extension=/usr/local/lib/php/extensions/no-debug-non-zts-20190902/xdebug.so" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini
RUN echo "error_reporting = E_ALL" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini \
  && echo "display_startup_errors = On" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini \
  && echo "display_errors = On" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini \
  && echo "xdebug.idekey=\"$XDEBUG_IDKEY\"" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini \
  && echo "xdebug.mode=develop,debug" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini \
  && echo "xdebug.start_with_request=yes" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini \
  && echo "xdebug.client_port=$XDEBUG_PORT" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini \
  && echo "xdebug.client_host=$XDEBUG_HOST" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini \
  && echo "xdebug.trigger_value=$XDEBUG_TRIGGERVALUE" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini

# mailhog sendmail
RUN apt-get update && apt-get install --no-install-recommends --assume-yes --quiet ca-certificates curl git && rm -rf /var/lib/apt/lists/*
RUN curl -Lsf 'https://storage.googleapis.com/golang/go1.8.3.linux-amd64.tar.gz' | tar -C '/usr/local' -xvzf -

ENV PATH /usr/local/go/bin:$PATH

RUN go get github.com/mailhog/mhsendmail && cp /root/go/bin/mhsendmail /usr/bin/mhsendmail \
  && echo "sendmail_path = /usr/bin/mhsendmail --smtp-addr $MAIL_HOST:$MAIL_PORT" > /usr/local/etc/php/conf.d/sendmail.ini

RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');" &&\
  php -r "if (hash_file('sha384', 'composer-setup.php') === 'dac665fdc30fdd8ec78b38b9800061b4150413ff2e3b6f88543c636f7cd84f6db9189d43a81e5503cda447da73c7e5b6') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;" &&\
  php composer-setup.php &&\
  php -r "unlink('composer-setup.php');"

# SETUP PHP-FPM CONFIG SETTINGS (max_children / max_requests)
RUN echo 'pm.max_children = 15' >> /usr/local/etc/php-fpm.d/zz-docker.conf && \
  echo 'pm.max_requests = 500' >> /usr/local/etc/php-fpm.d/zz-docker.conf

# RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini" \
# && sed -e 's/max_execution_time = 30/max_execution_time = 600/' -i "$PHP_INI_DIR/php.ini"

RUN mv composer.phar /usr/local/bin/composer && composer self-update

RUN curl -1sLf 'https://dl.cloudsmith.io/public/symfony/stable/setup.deb.sh' | bash
#RUN chmod +x setup.deb.sh
#RUN ./setup.deb.sh
RUN apt install symfony-cli

RUN apt install python3
RUN apt-get -y install python3-pip

# Copy existing application directory contents
#COPY ./api /var/www
VOLUME [ $APP_PATH ]

#RUN cat /usr/local/etc/php-fpm.d/www.conf

# Copy existing application directory contents
#COPY ./infra/php/local.ini ./infra/php/xdebug.ini /usr/local/etc/php/conf.d/
COPY ./infra/php/local.ini /usr/local/etc/php/conf.d/

RUN echo '\nexport GPG_TTY=$(tty)' >> ~/.bashrc
RUN . ~/.bashrc

# Expose port 9000 and start php-fpm server
EXPOSE $PHP_PORT
CMD ["php-fpm"]
