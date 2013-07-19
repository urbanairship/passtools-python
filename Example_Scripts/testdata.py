class TestData:
    def __init__(self):
        self.template_headers = """ {
        "headers":{
                      "barcodeAltText":{
                          "formatType":1,
                          "fieldType":"barcode",
                          "value":"123456789"
                      },
                      "icon_image":{
                          "formatType":1,
                          "fieldType":"topLevel",
                          "value":"https:\/\/s3.amazonaws.com\/passtools-localhost\/1\/images\/3c0f1c994b46cfc032147893ed4a00ba75a0d428_logo@2x.png"
                      },
                      "transitType":{
                          "formatType":1,
                          "fieldType":"passTop",
                          "value":"transitTypeAir"
                      },
                      "footer_image":{
                          "formatType":1,
                          "fieldType":"image",
                          "value":"https:\/\/s3.amazonaws.com\/passtools-localhost\/1\/images\/default-pass-footer.png"
                      },
                      "logo_image":{
                          "formatType":1,
                          "fieldType":"topLevel",
                          "value":"https:\/\/s3.amazonaws.com\/passtools-localhost\/1\/images\/default-pass-logo.png"
                      },
                      "barcode_label":{
                          "formatType":1,
                          "fieldType":"barcode",
                          "value":"Member ID"
                      },
                      "logo_color":{
                          "formatType":1,
                          "fieldType":"topLevel",
                          "value":"rgb(24,86,148)"
                      },
                      "logo_text":{
                          "formatType":1,
                          "fieldType":"topLevel",
                          "value":"Atlantis Airlines11"
                      },
                      "barcode_value":{
                          "formatType":1,
                          "fieldType":"barcode",
                          "value":"123456789"
                      },
                      "barcode_encoding":{
                          "formatType":1,
                          "fieldType":"barcode",
                          "value":"iso-8859-1"
                      },
                      "barcode_type":{
                          "formatType":1,
                          "fieldType":"barcode",
                          "value":"PKBarcodeFormatPDF417"
                      },
                      "background_color":{
                          "formatType":1,
                          "fieldType":"topLevel",
                          "value":"rgb(0,147,201)"
                      },
                      "foreground_color":{
                          "formatType":1,
                          "fieldType":"topLevel",
                          "value":"rgb(255,255,255)"
                      }
                  }
                  }
                  """

        self.template_fields = """ {
                "fields":{
                      "Merchant Website":{
                          "formatType":"URL",
                          "changeMessage":"",
                          "order":2,
                          "fieldType":"back",
                          "value":"http:\/\/www.test.com",
                          "label":"Merchant Website"
                          },
                      "Seat":{
                          "formatType":"String",
                          "changeMessage":"",
                          "order":2,
                          "fieldType":"secondary",
                          "textAlignment":"textAlignmentNatural",
                          "value":"26A",
                          "label":"Seat"
                      },
                      "Class":{
                          "formatType":"String",
                          "changeMessage":"",
                          "order":3,
                          "fieldType":"auxiliary",
                          "textAlignment":"textAlignmentNatural",
                          "value":"Econ",
                          "label":"Class"
                      },
                      "Terminal Gate":{
                          "formatType":"Number",
                          "changeMessage":"",
                          "order":1,
                          "numberStyle":"numberStyleDecimal",
                          "fieldType":"header",
                          "textAlignment":"textAlignmentNatural",
                          "value":11.0,
                          "label":"Terminal Gate"
                      },
                      "Arrival Airport":{
                          "formatType":"String",
                          "changeMessage":"",
                          "order":2,
                          "fieldType":"primary",
                          "textAlignment":"textAlignmentNatural",
                          "value":"SFO",
                          "label":"Arrival Airport"
                      },
                      "Ticket Number":{
                          "formatType":"Number",
                          "changeMessage":"",
                          "order":3,
                          "numberStyle":"numberStyleDecimal",
                          "fieldType":"secondary",
                          "textAlignment":"textAlignmentNatural",
                          "value":384013.0,
                          "label":"Ticket Number"
                      },
                      "Flight Number":{
                          "formatType":"String",
                          "changeMessage":"",
                          "order":2,
                          "fieldType":"auxiliary",
                          "textAlignment":"textAlignmentNatural",
                          "value":"G6A",
                          "label":"Flight Number"
                      },
                      "Passenger":{
                          "formatType":"String",
                          "changeMessage":"",
                          "order":1,
                          "fieldType":"secondary",
                          "textAlignment":"textAlignmentNatural",
                          "value":"First Last",
                          "label":"Passenger"
                      },
                      "Departure Airport":{
                          "formatType":"String",
                          "changeMessage":"",
                          "order":1,
                          "fieldType":"primary",
                          "textAlignment":"textAlignmentLeft",
                          "value":"LAX",
                          "label":"Departure Airport"
                      },
                      "Boarding Pass Details":{
                          "formatType":"String",
                          "changeMessage":"",
                          "order":1,
                          "fieldType":"back",
                          "value":"Some information about how this boarding pass works and how to use it.Additional terms and support information.",
                          "label":"Boarding Pass Details"
                      },
                      "Depart Time":{
                          "formatType":"String",
                          "changeMessage":"",
                          "order":1,
                          "fieldType":"auxiliary",
                          "textAlignment":"textAlignmentNatural",
                          "value":"10:40 AM",
                          "label":"Depart Time"
                      }
                   }
                  }
                """
