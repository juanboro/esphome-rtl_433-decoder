#include "esphome/core/log.h"

#include "rtl_433.h"

namespace esphome {
namespace rtl_433 {

static const char *const RTAG = "RTL_433";

void RTL433Decoder::setup() {
  rd.setCallback(&RTL433Decoder::process);
  rd.rtlSetup();
  ESP_LOGD(RTAG, "rtl_433 setup done");
}

void RTL433Decoder::recv_raw(esphome::remote_base::RawTimings& rawdata) {
  ESP_LOGD(RTAG, "sending raw receive data to rtl_433 signal decoder");
  rd.processRaw(rawdata, (void *) this);
}

bool RTL433Decoder::on_receive(remote_base::RemoteReceiveData data) {
  if (data.size() < 10)
    return false;  // reject anything that rtl_433 likely won't do anything with

  rd.processRaw(data.get_raw_data(), (void *) this);

  return true; // it's not really clear what this boolean is for exactly...
}

void RTL433Decoder::process(char *msg, void *ctx) {
  RTL433Decoder *objinst = (RTL433Decoder *) ctx;
  ESP_LOGD(RTAG, "Received msg: %s", msg);

  json::parse_json((const uint8_t* ) msg, strlen(msg),[objinst](JsonObject doc) {
    for (auto *trigger : objinst->triggers_onjsonmsg_) {
      trigger->trigger(doc);
    }
    return true;
  });

  free(msg); 

}

}
}
