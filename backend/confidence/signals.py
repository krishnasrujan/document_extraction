from backend.align.aligner import align_value



def ocr_signal(field, tokens):


    if not isinstance(
        field.value,
        (str, int, float)
    ):

        return {

            "name":"ocr_alignment",

            "score":0.5,

            "weight":0.5,

            "reason":
            "complex entity skipped"

        }



    aligned = align_value(

        field.value,

        tokens

    )



    if aligned is None:


        return {


            "name":"ocr_alignment",

            "score":0.0,

            "weight":0.5,

            "reason":
            "no OCR match"


        }



    return {


        "name":"ocr_alignment",


        "score":

            aligned["match_ratio"]

            *

            aligned["ocr_conf"],



        "weight":0.5,


        "reason":

            "OCR value aligned"

    }



def extraction_signal(field):


    if field.value is not None:


        return {

            "name":"extraction",

            "score":1.0,

            "weight":0.5,

            "reason":
            "value extracted"

        }



    return {

        "name":"extraction",

        "score":0.0,

        "weight":0.5,

        "reason":
        "missing value"

    }