import esphome.codegen as cg
from esphome import automation
import esphome.config_validation as cv
from esphome.const import (
    CONF_ON_JSON_MESSAGE,
    CONF_TRIGGER_ID,
    CONF_ID
)
from esphome.core import CORE

def AUTO_LOAD():
    if CORE.is_esp8266 or CORE.is_libretiny:
        return ["async_tcp", "json"]
    return ["json"]

rtl433_ns = cg.esphome_ns.namespace('rtl_433')
RTL433Decoder = rtl433_ns.class_('RTL433Decoder', cg.Component)

RTL433Trigger = rtl433_ns.class_(
    "RTL433Trigger", automation.Trigger.template(cg.JsonObjectConst)
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(RTL433Decoder),
        cv.Optional(CONF_ON_JSON_MESSAGE): automation.validate_automation(
            {
                cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(RTL433Trigger),
            }
        ),
    }
).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    for conf in config.get(CONF_ON_JSON_MESSAGE, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID])
        cg.add(var.register_onjsonmessage_trigger(trigger))
        await automation.build_automation(trigger, [(cg.JsonObjectConst, "x")], conf)

