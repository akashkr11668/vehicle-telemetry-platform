# BUILD STAGE

FROM ubuntu:22.04 AS builder

RUN apt-get update && apt-get install -y \
    g++ \
    cmake

WORKDIR /app

COPY . .

RUN rm -rf build && mkdir build

WORKDIR /app/build

RUN cmake ..

RUN make

# RUNTIME STAGE

FROM ubuntu:22.04

WORKDIR /app

COPY --from=builder /app/build/telemetry_engine .

CMD ["./telemetry_engine"]