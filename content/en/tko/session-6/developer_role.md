---
title: Developer Role
linkTitle: Developer Role
weight: 4
draft: true
---

## 1. Now let's play the role of the developer

As a developer we must debug the function products:ProductResource.getAllProducts to find the problem.

Now find the needle in Haystack !

``` bash
vi products/src/main/java/com/shabushabu/javashop/products/resources/ProductResource.java
```

Find getAllProducts `/getAllProducts`

scroll way... down!

``` java
public class ProductResource {

    private ProductService productService;

    @Inject
    public ProductResource(ProductService productService) {
        this.productService = productService;
    }

    @GET
    public Response getAllProducts(@DefaultValue("California") @QueryParam("location") String location) {
    
        // STEP X: All we know right now is somewhere in this function, latency was introduced.
  
        myCoolFunction1(location);
        myCoolFunction2(location);
        myCoolFunction10(location);
        myCoolFunction13(location);
        myCoolFunction5(location);
        myCoolFunction6(location);

        myCoolFunction7(location);
        myCoolFunction8(location);
        myCoolFunction9(location);

        myCoolFunction10(location);
        myCoolFunction11(location);
        myCoolFunction12(location);
        //something in HAYSTACK
        //something in HAYSTACK
        //something in HAYSTACK
```

Exit vi `:q!`

OK, enough fun... let's make this easier for our developer.
