import re
from rapidfuzz import fuzz


def normalize(value):

    if value is None:
        return ""


    if not isinstance(
        value,
        str
    ):

        value = str(value)


    return re.sub(
        r"\s+",
        "",
        value.lower()
    )



def align_value(value, tokens):

    target = normalize(value)


    if not target:

        return None


    best_score = 0

    best = None



    for start in range(
        len(tokens)
    ):


        text = ""

        bbox = None

        confidences = []



        for end in range(

            start,

            min(
                start + 6,
                len(tokens)
            )

        ):


            token = tokens[end]


            text += token.text


            confidences.append(
                token.conf
            )


            bbox = (

                token.bbox

                if bbox is None

                else bbox.union(
                    token.bbox
                )

            )



            score = fuzz.ratio(

                target,

                normalize(text)

            ) / 100



            if score > best_score:


                best_score = score


                best = (

                    bbox,

                    sum(confidences)
                    /
                    len(confidences),

                    text

                )



    if best is None:

        return None



    return {

        "bbox":best[0],

        "ocr_conf":best[1],

        "match_ratio":best_score,

        "text":best[2]

    }