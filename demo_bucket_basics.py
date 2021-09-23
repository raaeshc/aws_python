'''Create List and Delete Buckets '''
'''This code will incur some charges in your aws account'''
import sys
import boto3
from botocore.exceptions import ClientError


def get_s3(region=None):
    return boto3.resource('s3',region_name=region) if region else boto3.resource('s3')
    print("hi")

def list_my_buckets(s3):
    print('Buckets:\n\t',*[b.name for b in  s3.buckets.all()],sep="\n\t")

#list_my_buckets(s3_resource)


def create_and_delete_my_bucket(bucket_name,region,keep_bucket):
    s3=get_s3(region)
    print("Region is ",s3)
    list_my_buckets(s3)

    try:
        print("\Creating New bucket",bucket_name)
        bucket=s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint':region
            }
        )

    except ClientError as e:
        print(e)
        sys.exit('Exiting the script because the '
                 'bucket creation failed')

    bucket.wait_until_exists()
    print("This is new list",list_my_buckets(s3))

    if not keep_bucket:
        print('\n Deleting Bucket:',bucket.name)
        bucket.delete()

        bucket.wait_until_not_exists()
        print("After Deletion",list_my_buckets(s3))
    else:
        print("\n Keeping Bucket",bucket.name)

#create_and_delete_my_bucket('sample7909','us-east-2','t1 or any text')
#create_and_delete_my_bucket('sample7909','us-east-2','')


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('bucket_name',help="The name of the bucket to create")
    parser.add_argument('region',help='The region in which to create bucket')
    parser.add_argument('keep bucket',help='Keeps the created.When not specified the bucket is deleted '
                                             'bucket ',
                        action='store_true')
    args=parser.parse_args()
    create_and_delete_my_bucket(args.bucket_name,args.region,args.keep_bucket)


if __name__=='__main__':
    main()
