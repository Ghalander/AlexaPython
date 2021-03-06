#Boto is an AWS SDK for python used for amazon services
import boto3

# --------------- Main handler ------------------
def lambda_handler(event, context):


    dynamodb = boto3.resource('dynamodb')
    studentTable = dynamodb.Table('STUDENTS')
    session = event['session']
    session['attributes'] = {}

    if event['request']['type'] == "LaunchRequest":
        return Greeting(event, session)

    intent_name = event['request']['intent']['name']
    if intent_name == 'SetStudentInfoIntent':
        return SetStudentInfo(event, session, studentTable)
    elif intent_name == 'GetStudentInfoIntent':
        return GetStudentInfo(event, session, studentTable)
    elif intent_name == 'GiveStudentStarIntent':
        return GiveStudentStar(event, session, studentTable)
    elif intent_name == 'DeleteStudentIntent':
        return DeleteStudent(event, session, studentTable)

# --------------- Functions that control the skill's behavior ------------------
def Greeting(event, session):
    sentence = "Welcome to the star roster, what are we working with today?"
    return response(sentence, session['attributes'], False)

def SetStudentInfo(event, session, studentTable):
    studentname = event['request']['intent']['slots']['setName']['value']
    studentTable.put_item(Item={'name': studentname, 'stars': 0})
    sentence = "Ok, I have included a new student named " + studentname
    return response(sentence, session['attributes'], False)

def GetStudentInfo(event, session, studentTable):
    studentname = event['request']['intent']['slots']['getName']['value']
    data = studentTable.get_item(Key={'name': studentname})
    sentence = studentname + " has only " + str(data['Item']['stars']) + " gold stars"
    return response(sentence, session['attributes'], False)

def GiveStudentStar(event, session, studentTable):
    studentname = event['request']['intent']['slots']['giveName']['value']
    added_stars = event['request']['intent']['slots']['giveStar']['value']
    data = studentTable.get_item(Key={'name': studentname})
    starscore = data['Item']['stars'] + int(added_stars)
    studentTable.update_item(
        Key={'name': studentname},
        UpdateExpression='SET stars = :val1',
        ExpressionAttributeValues={':val1': starscore}
        )
    sentence = "The stars have been updated. " + studentname + " now has " + str(starscore) + " stars!"
    return response(sentence, session['attributes'], False)

def DeleteStudent(event, session, studentTable):
     studentname = event['request']['intent']['slots']['deleteName']['value']
     studentTable.delete_item( Key= {"name": studentname} )
     sentence = "Successfully removed " + studentname + " from our class"
     return response(sentence, session['attributes'], False)


# --------------- Helper that builds all of the responses ----------------------
def response(text, session_attributes, should_end_session):
    return {
    "version": "1.0",
     "response": {
      "outputSpeech": {
       "text": text,
       "type": "PlainText"
      },
     "speechletResponse": {
      "outputSpeech": {
       "text": text
      },
      "shouldEndSession": should_end_session
      }
     },
    "sessionAttributes": session_attributes
    }
