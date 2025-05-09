package loansrus.loanservice;

import java.util.concurrent.atomic.AtomicLong;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import java.math.BigDecimal;
import java.lang.System;

import org.springframework.kafka.core.KafkaTemplate;

@RestController
public class LoanController {

    // static final String DB_URL = "jdbc:mysql://localhost/MyDB";
    static final String DB_URL =  System.getenv("DB_URL");
    static final String USER = "MyUser";
    static final String PASS = "MyPassword";
    static final String INSERT_QUERY = "insert into MyDB.Loans values (?, ?)";

    private KafkaTemplate<String, String> template;

    public LoanController(KafkaTemplate<String, String> template) {
        this.template = template;
    }

    @GetMapping("/loanRequest")
    public String processLoanRequest(@RequestParam(value = "applicantId") String applicantId,
                                          @RequestParam(value = "loanAmount") long loanAmount) {

        Connection conn = null;
        PreparedStatement ps = null;

        try{
            conn = DriverManager.getConnection(DB_URL, USER, PASS);

            ps = conn.prepareStatement(INSERT_QUERY);
            ps.setString (1, applicantId);
            ps.setLong(2, loanAmount);

            ps.execute();
            System.out.println(String.format("Added a loan in the amount of %d to the database.", loanAmount));

        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            if (ps != null) {
                try {
                    ps.close();
                } catch (SQLException e) { /* Ignored */}
            }
            if (conn != null) {
                try {
                    conn.close();
                } catch (SQLException e) { /* Ignored */}
            }
        }

        try {
	    // add the loan to the kafka loan-events topics for further processing
	    String message = String.format("ApplicantId %s is requesting a loan in the amount of %d", applicantId, loanAmount);
	    template.send("loan-events", message);
	}
	catch (Exception e) {
	    e.printStackTrace();
	}

	return String.format("Loan in the amount of %d was processed successfully.", loanAmount);
    }
}
