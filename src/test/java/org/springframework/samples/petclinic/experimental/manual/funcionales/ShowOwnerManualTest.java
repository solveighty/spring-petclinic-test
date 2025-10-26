package org.springframework.samples.petclinic.owner;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.view;

import java.beans.Transient;

@SpringBootTest
@AutoConfigureMockMvc
class ShowOwnerManualTest {

	@Autowired
	private MockMvc mockMvc;

	// Retorna OK cuando el owner existe
	@Test
	void shouldReturnOkWhenOwnerExists() throws Exception {
		mockMvc.perform(get("/owners/1")).andExpect(status().isOk()).andExpect(view().name("owners/ownerDetails"));
	}

	// Retorna Internal Server Error o 500 cuando el owner no existe
	@Test
	void shouldReturnServerErrorWhenOwnerNotFound() throws Exception {
		mockMvc.perform(get("/owners/11")).andExpect(status().isInternalServerError());
	}

	// Retorna Bad Request o 400 cuando el id del owner es invalido
	@Test
	void shouldReturnBadRequestWhenOwnerIdIsInvalid() throws Exception {
		mockMvc.perform(get("/owners/testing")).andExpect(status().isBadRequest());
	}

	// Retorna Internal Server Error o 500 cuando el id del owner es negativo
	@Test
	void shouldReturnServerErrorWhenOwnerIdIsNegative() throws Exception {
		mockMvc.perform(get("/owners/-1")).andExpect(status().isInternalServerError());
	}

}