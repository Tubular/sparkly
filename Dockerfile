#
# Copyright 2017 Tubular Labs, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Java 11 comes from Temurin rather than Debian: Spark 3.2 supports Java 8 and 11
# only, and no Debian release still in support carries an openjdk-11 package.
FROM eclipse-temurin:11-jdk AS jdk

# Pinned to a Debian release rather than the floating tag: `python:3.10` now
# resolves to trixie, which the previous stretch-era apt sources did not survive.
FROM python:3.10-bookworm

LABEL maintainer="dev@tubularlabs.com"

COPY --from=jdk /opt/java/openjdk /opt/java/openjdk
ENV JAVA_HOME=/opt/java/openjdk
ENV PATH="/opt/java/openjdk/bin:${PATH}"

# Python env
ENV CASS_DRIVER_NO_EXTENSIONS=1
COPY requirements.txt /tmp/requirements.txt
COPY requirements_dev.txt /tmp/requirements_dev.txt
COPY requirements_extras.txt /tmp/requirements_extras.txt
RUN python -m pip install -r /tmp/requirements.txt
RUN python -m pip install -r /tmp/requirements_dev.txt
RUN python -m pip install -r /tmp/requirements_extras.txt

# Provision Sparkly
ADD . /opt/sparkly/
WORKDIR /opt/sparkly/
