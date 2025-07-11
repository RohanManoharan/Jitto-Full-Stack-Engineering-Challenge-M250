# Jitto-Full-Stack-Engineering-Challenge-M250
Task: Create two AWS API Gateway connected to AWS Lambda functions that:
- Uploads images to an S3 bucket that are labelled "cat" or "dog".
- Retrieves a random image based on the given label.

## Image Upload Endpoint
- POST https://ijqdv8kn3a.execute-api.ca-central-1.amazonaws.com/dev/upload
- Headers need to be supplied, such as content-type and image label.

```
curl -X POST \
  "https://ijqdv8kn3a.execute-api.ca-central-1.amazonaws.com/dev/upload" \
  -H "Content-Type: image/jpeg" \
  -H "x-amz-meta-pet: cat" \
  --data-binary @your-image-file.jpg
```

- Alternatively, you can use postman instead.

## Random Image Retrieval Endpoint
- GET https://ijqdv8kn3a.execute-api.ca-central-1.amazonaws.com/dev/random?label={label}
- Only valid arguments for label are "cat" and "dog"

```
curl -X GET \
  "https://ijqdv8kn3a.execute-api.ca-central-1.amazonaws.com/dev/random?label={label}"
```
- Once again, you can use postman instead.

## Design Choices
- In this challenge, I went and made many changes to what the current product is.
- I initially had a lambda function trigger when an object is added to an s3 bucket, which would then validate it, but later it caused issues and didn't work out.
- I also was unable to use POST as the HTTP request method because of this, but I was able to fix this later when I restructured the API.
- In the end I decided to make an Lambda function trigger when the API was called, which would then validify the file and later put it in a S3 bucket.
- I didn't really struggle with the next API Endpoint, as by then most of my struggles came from my earlier attempt.
- The random image retrieval lambda function validifies the label given, gets the bucket based on the label (/cat or /dog), selects a random file, and then returns a presigned URL, allowing the user to access their image.

## Costs
- Low Scale (1k responses per month)
  - Lambda: FREE
  - API Gateway: FREE (for the first year)
  - S3: ~$0.01-0.10
  - Total: ~$0.01-0.10

- Medium Scale Scenarios (100k responses per month)
  - Lambda: ~$2-8 depending on execution time
  - API Gateway: ~$35
  - S3: $2-20 depending on storage volume
  - Total: ~$40-65
 
- High Scale Scenarios (1M responses per month)
  - Lambda: ~$20-80 depending on execution time
  - API Gateway: ~$350
  - S3: $20-200 depending on storage volume
  - Total: ~$400-650
  
## Technical Challenges/Edge Cases
- Generally speaking, most of the learning was where my technical challenges lie. Working with AWS, configuring roles, testing code and api calls were what I struggled with the most. But this is to be expected for a first time learner. I've had trouble with receiving metadata headers because I was checking with the incorrect file.

- Some normal and extreme edge cases are as follows
  - Ensuring pet labels are only "dog" and "cat"
  - Validating content-type on upload
  - Filtering out key names that DONT end with / (EXTREME)
    - Ensures that directories aren't accidentally selected
  - Ensuring bucket of given label has files to be selected from

