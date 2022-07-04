# NVC API description

## wallets/{walletAddress}

### statusCode 200
```
{
	walletId:1,
	totalEarnInCurrentMonth:1230,// by $, lãi và gốc đã nhận trong tháng
}
```
### statusCode 400 => address sai định dạng
### statusCode 404 => k tìm thấy address trong database

## wallets/{walletId}/nfts/{nftId}
### statusCode 200
``` {
	currentOwner:"0x..",
	holdDaysInCurrentMonth: 3,//number of days the NFT owned by the owner
	collectionId: 1,
	earnings:[
		{
			month:1,//1-12, 
			principalEarned:12,//by $,gốc nhận được của tháng 1 
			interestEarned:0.1//by $, lãi nhận được của tháng 1
			interestRate:0.1//by %, % lãi của tháng
			principalRate:20//by $, tiền gốc mỗi NFT của tháng
		}
	]
} 
```
### statusCode 404 => k tìm thấy address/NFT trong database

## collections/{collectionId}
```
{
	from:"",
	to:"",
	name:"",
	updates[{
		from:"",
		interest:1.5,//by %, lãi mỗi NFT
		principal:20,//by $?, gốc mỗi NFT
	}]
}
```
### statusCode 404 => k tìm thấy collection trong database

## collections/{collectionId}/report
> Admin only

### statusCode 200
```
{
	uniqueHolders: 12,
	totalPay:123999,// By $, tong so lai va goc phai tra cho toan bo holders,
	estimate:,//tong so lai phai tra cho den ki end
}
```
### statusCode 403 => not admin
