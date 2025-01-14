FROM public.ecr.aws/lambda/python:3.9

# Set the working directory to the Lambda task root
WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY app.py "${LAMBDA_TASK_ROOT}"
COPY inference.py "${LAMBDA_TASK_ROOT}"
COPY query.py "${LAMBDA_TASK_ROOT}"
COPY utils.py "${LAMBDA_TASK_ROOT}"
CMD ["app.average_word_vector"]
