import os
import google.generativeai as genai
import dotenv
import json

dotenv.load_dotenv()

genai.configure(api_key=os.environ["API_KEY"])
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"


# Create the model
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel("gemini-1.5-flash")
modelpro = genai.GenerativeModel("gemini-2.0-flash-exp")


async def analyze_discounts_international(file, weeklyChargesBand):

    chat_sessionpro = modelpro.start_chat(history=[
        {
            "role":
            "user",
            "parts": [
                file,
                f"Use the attached contract to fill the table. the weekly charges band is {weeklyChargesBand}. DOMESTIC AIR SERVICE LEVEL WEIGHT RANGE CURRENT UPS\nNext Day Air Letter All\nNext Day Air Package All\nNext Day Air Saver Letter All\nNext Day Air Saver Package All\n2nd Day AM Letter All\n2nd Day AM Package All\n2nd Day Air Letter All\n2nd Day Air Package All\n3 Day Select Package All\nNext Day Air CWT All\nNext Day Air Saver CWT All\n2nd Day Air AM CWT All\n2nd Day Air CWT All\n3 Day Select CWT All",
            ],
        },
        {
            "role":
            "model",
            "parts": [
                "```json\n{\"Domestic Air Service Level\": {\"Next Day Air\": {\"Letter\": {\"Weight Range\": \"All\", \"Current UPS\": \"61.00%\"}, \"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"61.00%\"}}, \"Next Day Air Saver\": {\"Letter\": {\"Weight Range\": \"All\", \"Current UPS\": \"61.00%\"}, \"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"61.00%\"}}, \"2nd Day AM\": {\"Letter\": {\"Weight Range\": \"All\", \"Current UPS\": \"59.00%\"}, \"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"59.00%\"}}, \"2nd Day Air\": {\"Letter\": {\"Weight Range\": \"All\", \"Current UPS\": \"59.00%\"}, \"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"59.00%\"}}, \"3 Day Select\": {\"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"51.00%\"}}, \"Next Day Air CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}, \"Next Day Air Saver CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}, \"2nd Day AM CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}, \"2nd Day Air CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}, \"3 Day Select CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}}}\n```",
            ],
        },
    ])
    chat_session = model.start_chat(history=[
        {
            "role":
            "user",
            "parts": [
                file,
                f"Use the attached contract to fill the table. the weekly charges band is {weeklyChargesBand}. DOMESTIC AIR SERVICE LEVEL WEIGHT RANGE CURRENT UPS\nNext Day Air Letter All\nNext Day Air Package All\nNext Day Air Saver Letter All\nNext Day Air Saver Package All\n2nd Day AM Letter All\n2nd Day AM Package All\n2nd Day Air Letter All\n2nd Day Air Package All\n3 Day Select Package All\nNext Day Air CWT All\nNext Day Air Saver CWT All\n2nd Day Air AM CWT All\n2nd Day Air CWT All\n3 Day Select CWT All",
            ],
        },
        {
            "role":
            "model",
            "parts": [
                "```json\n{\"Domestic Air Service Level\": {\"Next Day Air\": {\"Letter\": {\"Weight Range\": \"All\", \"Current UPS\": \"61.00%\"}, \"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"61.00%\"}}, \"Next Day Air Saver\": {\"Letter\": {\"Weight Range\": \"All\", \"Current UPS\": \"61.00%\"}, \"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"61.00%\"}}, \"2nd Day AM\": {\"Letter\": {\"Weight Range\": \"All\", \"Current UPS\": \"59.00%\"}, \"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"59.00%\"}}, \"2nd Day Air\": {\"Letter\": {\"Weight Range\": \"All\", \"Current UPS\": \"59.00%\"}, \"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"59.00%\"}}, \"3 Day Select\": {\"Package\": {\"Weight Range\": \"All\", \"Current UPS\": \"51.00%\"}}, \"Next Day Air CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}, \"Next Day Air Saver CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}, \"2nd Day AM CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}, \"2nd Day Air CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}, \"3 Day Select CWT\": {\"Weight Range\": \"All\", \"Current UPS\": null}}}\n```",
            ],
        },
    ])

    international1 = chat_sessionpro.send_message(
        '''Use the attached contract to fill the table. The weekly charges bands ($) is {weeklyChargesBand}. (please return values related to this alone). return in a json format and only the json of the table and nothing else. 

            {
              "INTERNATIONAL SERVICE LEVEL": {
                "Export": {
                  "UPS Worldwide Express®": {
                    "Letter": {
                      "Weight Range": "All",
                      "Current UPS": ""
                    },
                    "Document": {
                      "Weight Range": "All",
                      "Current UPS": ""
                    },
                    "Pak": {
                      "Weight Range": "All",
                      "Current UPS": ""
                    },
                    "Package": {
                      "Weight Range": "All",
                      "Current UPS": ""
                    }
                  },
                  "UPS Worldwide Saver®": {
                    "Letter": {
                      "Weight Range": "All",
                      "Current UPS": ""
                    },
                    "Document": {
                      "Weight Range": "All",
                      "Current UPS": ""
                    },
                    "Pak": {
                      "Weight Range": "All",
                      "Current UPS": ""
                    },
                    "Package": {
                      "Weight Range": "All",
                      "Current UPS": ""
                    }
                  },
                  "UPS Worldwide Expedited®": {
                    "Document": {
                      "Weight Range": "All",
                      "Current UPS": ""
                    },
                    "Package": {
                      "Weight Range": "All",
                      "Current UPS": ""
                    }
                  },
                  "UPS® Standard to Canada": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  },
                  "UPS® Standard to Mexico": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  }
                },
                "Import": {
                  "UPS Worldwide Express®": {
                    "Letter": {
                      "Weight Range": "All",
                      "Current UPS": ""
                    },
                    "Document": {
                      "Weight Range": "All",
                      "Current UPS": ""
                    },
                    "Package": {
                      "Weight Range": "All",
                      "Current UPS": ""
                    }
                  },
                  "UPS Worldwide Saver®": {
                    "Letter": {
                      "Weight Range": "All",
                      "Current UPS": ""
                    },
                    "Document": {
                      "Weight Range": "All",
                      "Current UPS": ""
                    },
                    "Package": {
                      "Weight Range": "All",
                      "Current UPS": ""
                    }
                  },
                  "UPS Worldwide Expedited®": {
                    "Package": {
                      "Weight Range": "All",
                      "Current UPS": ""
                    }
                  },
                  "UPS® Standard from Canada": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  },
                  "UPS® Standard from Mexico": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  }
                }
              }
            }

            ''')  # Note closing parentheses adjusted."

    international2 = chat_sessionpro.send_message(
        '''Use the attached contract to fill the table. return in a json format and only the json of the table and nothing else. 

            {
              "International Service Level": {
                "Export UPS Worldwide Express®": {
                  "Letter - Incentives Off Effective Rates": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  },
                  "Document - Incentives Off Effective Rates": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  },
                  "Pak - Incentives Off Effective Rates": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  },
                  "Package - Incentives Off Effective Rates": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  }
                },
                "Export UPS Worldwide Saver®": {
                  "Letter - Incentives Off Effective Rates": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  },
                  "Document - Incentives Off Effective Rates": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  },
                  "Pak - Incentives Off Effective Rates": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  },
                  "Package - Incentives Off Effective Rates": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  }
                },
                "Export UPS Worldwide Expedited®": {
                  "Document - Incentives Off Effective Rates": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  },
                  "Package - Incentives Off Effective Rates": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  }
                },
                "Import UPS Worldwide Express®": {
                  "Letter - Incentives Off Effective Rates": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  },
                  "Document - Incentives Off Effective Rates": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  },
                  "Package - Incentives Off Effective Rates": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  }
                },
                "Import UPS Worldwide Saver®": {
                  "Letter - Incentives Off Effective Rates": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  },
                  "Document - Incentives Off Effective Rates": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  },
                  "Package - Incentives Off Effective Rates": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  }
                },
                "Import UPS Worldwide Expedited®": {
                  "Package - Incentives Off Effective Rates": {
                    "Weight Range": "All",
                    "Current UPS": ""
                  }
                }
              }
            }


            ''')  # Note closing parentheses adjusted."

    messageadd = "Use the attached contract to fill the table. return in a json format and only the json of the table and nothing else. add values from" + str(
        international1
    ) + "and the corresponding incentive off values from" + str(
        international2
    ) + '''. add corresponding values to a consolidated table of this json format: Here is the JSON with percentages removed and replaced with empty strings:

        ```json
        {
          "INTERNATIONAL SERVICE LEVEL": {
            "Export": {
              "UPS Worldwide Express®": {
                "Letter": {
                  "Weight Range": "All",
                  "Current UPS": "",
                  "Incentives Off Effective Rates": ""
                },
                "Document": {
                  "Weight Range": "All",
                  "Current UPS": "",
                  "Incentives Off Effective Rates": ""
                },
                "Pak": {
                  "Weight Range": "All",
                  "Current UPS": "",
                  "Incentives Off Effective Rates": ""
                },
                "Package": {
                  "Weight Range": "All",
                  "Current UPS": "",
                  "Incentives Off Effective Rates": ""
                }
              },
              "UPS Worldwide Saver®": {
                "Letter": {
                  "Weight Range": "All",
                  "Current UPS": "",
                  "Incentives Off Effective Rates": ""
                },
                "Document": {
                  "Weight Range": "All",
                  "Current UPS": "",
                  "Incentives Off Effective Rates": ""
                },
                "Pak": {
                  "Weight Range": "All",
                  "Current UPS": "",
                  "Incentives Off Effective Rates": ""
                },
                "Package": {
                  "Weight Range": "All",
                  "Current UPS": "",
                  "Incentives Off Effective Rates": ""
                }
              },
              "UPS Worldwide Expedited®": {
                "Document": {
                  "Weight Range": "All",
                  "Current UPS": "",
                  "Incentives Off Effective Rates": ""
                },
                "Package": {
                  "Weight Range": "All",
                  "Current UPS": "",
                  "Incentives Off Effective Rates": ""
                }
              },
              "UPS® Standard to Canada": {
                "Weight Range": "All",
                "Current UPS": ""
              },
              "UPS® Standard to Mexico": {
                "Weight Range": "All",
                "Current UPS": ""
              }
            },
            "Import": {
              "UPS Worldwide Express®": {
                "Letter": {
                  "Weight Range": "All",
                  "Current UPS": "",
                  "Incentives Off Effective Rates": ""
                },
                "Document": {
                  "Weight Range": "All",
                  "Current UPS": "",
                  "Incentives Off Effective Rates": ""
                },
                "Package": {
                  "Weight Range": "All",
                  "Current UPS": "",
                  "Incentives Off Effective Rates": ""
                }
              },
              "UPS Worldwide Saver®": {
                "Letter": {
                  "Weight Range": "All",
                  "Current UPS": "",
                  "Incentives Off Effective Rates": ""
                },
                "Document": {
                  "Weight Range": "All",
                  "Current UPS": "",
                  "Incentives Off Effective Rates": ""
                },
                "Package": {
                  "Weight Range": "All",
                  "Current UPS": "",
                  "Incentives Off Effective Rates": ""
                }
              },
              "UPS Worldwide Expedited®": {
                "Package": {
                  "Weight Range": "All",
                  "Current UPS": "",
                  "Incentives Off Effective Rates": ""
                }
              },
              "UPS® Standard from Canada": {
                "Weight Range": "All",
                "Current UPS": ""
              },
              "UPS® Standard from Mexico": {
                "Weight Range": "All",
                "Current UPS": ""
              }
            }
          }
        }'''

    response5 = chat_session.send_message(
        messageadd)  # Note closing parentheses adjusted."

    international1 = json.loads(international1.text.replace(
        '```json\n', '').replace('\n```', ''))
    international2 = json.loads(international2.text.replace(
        '```json\n', '').replace('\n```', ''))
    response5 = json.loads(response5.text.replace(
        '```json\n', '').replace('\n```', ''))

    return international1, international2, response5
