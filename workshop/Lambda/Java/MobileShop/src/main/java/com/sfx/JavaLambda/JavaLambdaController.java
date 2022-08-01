package com.sfx.JavaLambda;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectReader;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.client.RestTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import java.util.*;
import java.io.IOException;
import java.rmi.server.UID;


@Controller
public class JavaLambdaController {

	// setting up the URL top call - (replace it with proper call once that is deployed)
	String url = "REPLACE WITH RETAILORDER URL";
		
	// setting up some fields for span.tags
	private UID orderNumber = new UID();
	private String version = "1.1"; // example fields that will be passed as tags

	private final Logger LOG = LoggerFactory.getLogger(this.getClass());

	@Autowired
	RestTemplate restTemplate;

	@Bean
	public RestTemplate getRestTemplate() {
		return new RestTemplate();
	}

	@GetMapping("/order")
	public String orderForm(Model model) {
		// Set up initial values for html form
		model.addAttribute("order", new Order());
		return "order"; // view
	}

	@PostMapping("/order")
	public String orderSubmit(@ModelAttribute Order Order, Model model) throws IOException  {
		LOG.info("Inside OrderSubmit");
		//span.tag("Version", version); // sending tag along in the span. useful for development
		//span.tag("orderNumber", orderNumber.toString());
	
		LOG.info("Order:");
		LOG.info("phoneType : " + Order.getPhoneType());
		LOG.info("Quantity  : " + Order.getQuantity());
		LOG.info("Customer  : " + Order.getCustomerType());
         // More tags	
		//span.tag("phone",    Order.getPhoneType());
		//span.tag("Quantity",  String.valueOf(Order.getQuantity()));
		//span.tag("Customer", Order.getCustomerType());

		//going to check if the url is valid otherwise error
		if (url.startsWith("http")) {
			// create headers
			HttpHeaders headers = new HttpHeaders();
			// set `content-type` header
			headers.setContentType(MediaType.APPLICATION_JSON);
			// set `accept` header
			headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));
			// create a map for post parameters
			Map<String, Object> map = new HashMap<>();
			map.put("ProductName", Order.getPhoneType());
			map.put("Quantity",  Order.getQuantity());
			map.put("CustomerType", Order.getCustomerType());
			map.put("orderNumber",orderNumber.toString());
			// build the request
			HttpEntity<Map<String, Object>> orderRequest = new HttpEntity<>(map, headers);
			// send POST request
			ResponseEntity<String> returnedOrder = this.restTemplate.postForEntity(url, orderRequest, String.class);

			ObjectMapper objectMapper = new ObjectMapper();
			ObjectReader objectReader = objectMapper.readerForUpdating(Order);

			Order newOrder = objectReader.readValue(returnedOrder.getBody());
			LOG.info("The response received by the remote call is " + returnedOrder.toString());
			
			//capture the response and put it in a tag
			//span.tag("Lambda Response",returnedOrder.toString());
			
			model.addAttribute("order", newOrder);
			LOG.info("Leaving OrderSubmit");
			return "result";
			}
		else
		{	
			LOG.error("url not replaced with valid url to the RetailOrder Lambda!");
			return "error";
		}	
	}
}